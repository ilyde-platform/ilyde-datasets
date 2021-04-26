# -*- coding: utf-8 -*-
#
# Copyright (c) 2020-2021 Hopenly srl.
#
# This file is part of Ilyde.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest
import logging
import grpc
from google.protobuf.struct_pb2 import Struct
from grpc_interceptor.exceptions import GrpcException, InvalidArgument, NotFound, Unknown
from protos import dataset_pb2, dataset_pb2_grpc
import server

# setup logger
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.NOTSET, format=FORMAT)
logger = logging.getLogger(__name__)


class DatasetServicerTest(unittest.TestCase):

    def setUp(self):
        self._server, port = server.create_server('[::]:0')
        self._server.start()
        self._channel = grpc.insecure_channel('localhost:%d' % port)

    def tearDown(self):
        self._channel.close()
        self._server.stop(None)

    def test_create_dataset(self):
        logger.info("test create dataset")
        stub = dataset_pb2_grpc.DatasetServicesStub(self._channel)
        # prepare a payload
        payload = {
            'name': 'fashion-mnist-data',
            'description': 'Dataset di fashion 28x28.',
            'scope': "Global"
        }

        response = stub.CreateDataset(dataset_pb2.Dataset(**payload))
        self.assertTrue(response.id)
        self.assertTrue(response.create_at)
        self.assertEqual(response.name, payload['name'])

    def test_retrieve_dataset(self):
        logger.info("test retrieve dataset")
        stub = dataset_pb2_grpc.DatasetServicesStub(self._channel)
        # prepare a payload
        payload = {
            'name': 'fashion-mnist-data',
            'description': 'Dataset di fashion 28x28.',
            'scope': "Global"
        }

        dataset = stub.CreateDataset(dataset_pb2.Dataset(**payload))
        # verify if we can retrieve dataset
        response = stub.RetrieveDataset(dataset_pb2.ID(id=dataset.id))
        self.assertEqual(response.id, dataset.id)
        self.assertEqual(response.name, dataset.name)
        # verify raise of error when doesn't exists
        with self.assertRaises(grpc.RpcError) as cm:
            stub.RetrieveDataset(dataset_pb2.ID(id="my-id"))


if __name__ == '__main__':
    logger.info("tests DatasetsServicer")
    unittest.main(verbosity=2)


