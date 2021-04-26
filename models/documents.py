# encoding: utf-8
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
from mongoengine import *
import datetime


class File(EmbeddedDocument):
    name = StringField(required=True)
    size = LongField(required=True, min_value=0)


class Dataset(Document):
    """The object Dataset stored in the Database"""
    name = StringField(required=True)
    description = StringField(required=True, max_length=100)
    scope = StringField(required=True, max_length=100)
    project = StringField(max_length=100, default='')
    version = StringField(required=True, default='')
    deleted = BooleanField(default=False)
    create_at = DateTimeField(default=datetime.datetime.now)
    last_update = DateTimeField(default=datetime.datetime.now)

    meta = {
        'ordering': ['-create_at']
    }

    def __str__(self):
        return str(self.id)


class Version(Document):
    """docstring for Version."""
    name = StringField(required=True)
    dataset = ReferenceField(Dataset, required=True, reverse_delete_rule=2)
    related_bucket = StringField(required=True)
    bucket_tree = ListField(EmbeddedDocumentField(File), required=True)
    size = LongField(min_value=0, required=True)
    author = StringField(required=True)
    create_at = DateTimeField(default=datetime.datetime.now)
    meta = {
        'ordering': ['-create_at']
    }
