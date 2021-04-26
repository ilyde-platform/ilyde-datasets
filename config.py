# coding: utf-8
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

from decouple import config
import os

BASE_DIR = os.path.dirname(__file__)

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', cast=str)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', cast=str)

MINIO_HOST = config('MINIO_HOST')
MINIO_ENDPOINT = config('MINIO_ENDPOINT')

MONGO_DATABASE_URL = config('MONGO_DATABASE_URL')
MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')
