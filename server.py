# encoding: utf-8
import logging
from concurrent import futures
import grpc
import uuid

from grpc_health.v1 import health, health_pb2_grpc
from grpc_interceptor.exceptions import InvalidArgument

from interceptors import ExceptionToStatusInterceptor
from utils import increment_version, construct_mongo_query
from protos import dataset_pb2, dataset_pb2_grpc
from models import documents
from serializers import dataset_serializer, id_serializer, version_serializer, status_serializer, \
    search_dataset_request_serializer, search_dataset_response_serializer, search_version_request_serializer, \
    search_version_response_serializer

import datetime
import services

# setup logger
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class DatasetServicer(dataset_pb2_grpc.DatasetServicesServicer):

    def RetrieveDataset(self, request, context):
        data = id_serializer.load(request)
        dataset = documents.Dataset.objects(deleted=False).get(id=data['id'])

        return dataset_serializer.dump(dataset)

    def CreateDataset(self, request, context):
        # validate request payload
        data = dataset_serializer.load(request)
        dataset = documents.Dataset(name=data['name'],
                                    description=data['description'],
                                    scope=data['scope'],
                                    project=data['project']).save()
        return dataset_serializer.dump(dataset)

    def UpdateDataset(self, request, context):
        # validate request payload
        data = dataset_serializer.load(request)
        # validate id
        if not data.get('id'):
            raise InvalidArgument("Dataset's id not provided.")

        # retrieve dataset
        dataset = documents.Dataset.objects(deleted=False).get(id=data['id'])

        # update name and description.
        # other fields are immutable
        dataset.name = data['name']
        dataset.description = data['description']
        dataset.last_update = datetime.datetime.now()
        dataset.save()

        return dataset_serializer.dump(dataset)

    def DeleteDataset(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        dataset = documents.Dataset.objects(deleted=False).get(id=data['id'])
        dataset.deleted = True
        dataset.save()

        return status_serializer.dump({"status": 200, "message": "Successfully delete dataset."})

    def SearchDatasets(self, request, context):
        data = search_dataset_request_serializer.load(request)
        mappings = {
            "id": "_id",
            "name": "name",
            "scope": "scope",
            "project": "project"
        }
        ids = ["_id"]

        query = construct_mongo_query(data["query"], mappings, ids)
        if query:
            datasets = documents.Dataset.objects(__raw__=query).filter(deleted=False)
        else:
            datasets = documents.Dataset.objects(deleted=False)

        paginated = dataset_serializer.paginate(datasets, page=data["page"],
                                                limit=data["limit"])
        payload = {
            "total": len(datasets),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return search_dataset_response_serializer.dump(payload)

    def RetrieveVersion(self, request, context):
        # validate request payload
        data = id_serializer.load(request)
        version = documents.Version.objects(
            dataset__in=documents.Dataset.objects(deleted=False)).get(id=data['id'])
        return version_serializer.dump(version)

    def CreateVersion(self, request, context):
        # validate request payload
        data = version_serializer.load(request)
        # retrieve dataset
        dataset = documents.Dataset.objects(deleted=False).get(id=data['dataset'])
        last_version = documents.Version.objects(dataset=dataset.id).order_by('-name').first()
        if not last_version:
            last_version_name = '0'
        else:
            last_version_name = last_version.name

        next_version_name = increment_version(last_version_name)
        bucket_tree = services.list_minio_bucket_objects(data['related_bucket'])
        # size = reduce(lambda a, b: a['size'] + b['size'], bucket_tree)
        size = 0
        for file in bucket_tree:
            size += file['size']
        # save new version
        version = documents.Version(name=next_version_name, dataset=dataset.id, related_bucket=data['related_bucket'],
                                    bucket_tree=bucket_tree, size=size, author=data['author']).save()
        dataset.version = next_version_name
        dataset.last_update = datetime.datetime.now()
        dataset.save()

        return version_serializer.dump(version)

    def SearchVersions(self, request, context):
        data = search_version_request_serializer.load(request)
        mappings = {
            "id": "_id",
            "name": "name",
            "dataset": "dataset",
            "author": "author"
        }
        ids = ["_id", "dataset"]

        query = construct_mongo_query(data["query"], mappings, ids)
        if query:
            versions = documents.Version.objects(__raw__=query).filter(
                dataset__in=documents.Dataset.objects(deleted=False))
        else:
            versions = documents.Version.objects(
                dataset__in=documents.Dataset.objects(deleted=False))

        paginated = version_serializer.paginate(versions, page=data["page"],
                                                limit=data["limit"])
        payload = {
            "total": len(versions),
            "page": paginated[0],
            "limit": paginated[1],
            "data": paginated[2]
        }
        return search_version_response_serializer.dump(payload)

    def CreateBucket(self, request, context):
        # slugify and create dataset name to create a bucket_name
        bucket_name = uuid.uuid4().hex
        # minio create bucket
        services.create_minio_bucket(bucket_name)
        return dataset_pb2.Bucket(name=bucket_name)


def create_server(server_address):
    interceptors = [ExceptionToStatusInterceptor()]

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    dataset_pb2_grpc.add_DatasetServicesServicer_to_server(
        DatasetServicer(), server
    )
    # Create a health check servicer. We use the non-blocking implementation
    # to avoid thread starvation.
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=1))
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    port = server.add_insecure_port(server_address)
    return server, port


def serve():
    server, port = create_server('[::]:50051')
    server.start()
    logger.info("server is serving on port {} ............".format(port))
    server.wait_for_termination()
    logger.info("server is stopped............")


if __name__ == '__main__':
    logger.info("server is starting............")
    serve()
