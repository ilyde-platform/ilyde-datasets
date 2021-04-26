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



