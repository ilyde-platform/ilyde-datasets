# -*- coding: utf-8 -*-

from minio import Minio
import config


def get_minio_client():
    client = Minio(config.MINIO_HOST, access_key=config.AWS_ACCESS_KEY_ID,
                   secret_key=config.AWS_SECRET_ACCESS_KEY, secure=False)
    return client


def create_minio_bucket(bucket_name):
    minio = get_minio_client()
    minio.make_bucket(bucket_name, 'us-west-1')


def list_minio_bucket_objects(bucket_name):
    minio = get_minio_client()
    objects = minio.list_objects_v2(bucket_name, recursive=True)

    return [{'name': obj.object_name, 'size': obj.size} for obj in objects]



