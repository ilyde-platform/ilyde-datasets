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
from marshmallow import Schema, fields, pre_load, post_dump, validates_schema, ValidationError
from google.protobuf import json_format

from protos.dataset_pb2 import Dataset, Status, Version, ID, SearchVersionRequest, SearchDatasetRequest, \
    SearchVersionResponse, SearchDatasetResponse


class BaseSchema(Schema):
    # Custom options
    __proto_class__ = None
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    def parse_proto_message(self, message):
        return json_format.MessageToDict(message, **self.__decode_options__)

    @staticmethod
    def paginate(data, page: int, limit: int):
        begin = (page - 1) * limit
        end = begin + limit
        return page, limit, data[begin:end]

    @pre_load(pass_many=True)
    def decode(self, data, many, **kwargs):
        if many:
            return [self.parse_proto_message(message) for message in data]
        return self.parse_proto_message(data)

    @post_dump(pass_many=True)
    def encode(self, data, many, **kwargs):
        if many:
            return [self.__proto_class__(**message) for message in data]
        return self.__proto_class__(**data)


class DatasetSerializer(BaseSchema):
    __proto_class__ = Dataset

    id = fields.Str()
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    scope = fields.Str(missing="Local")
    project = fields.Str(missing="")
    version = fields.Str()
    create_at = fields.Str()
    last_update = fields.Str()

    @validates_schema
    def validate_scope(self, data, **kwargs):
        if data["scope"] == "Local" and not data["project"]:
            raise ValidationError("Local datasets must have project value set.")


class FileSerializer(Schema):
    name = fields.Str(required=True)
    size = fields.Int(required=True)


class StatusSerializer(BaseSchema):
    __proto_class__ = Status

    status = fields.Integer()
    message = fields.Str()


class VersionSerializer(BaseSchema):
    __proto_class__ = Version

    id = fields.Str()
    name = fields.Str()
    dataset = fields.Str(required=True)
    related_bucket = fields.Str(required=True)
    author = fields.Str(required=True)
    bucket_tree = fields.List(fields.Nested(FileSerializer))
    size = fields.Int()
    create_at = fields.Str()


class IDSerializer(BaseSchema):
    __proto_class__ = ID

    id = fields.Str(required=True)


class DatasetFilterSerializer(Schema):
    id = fields.Str()
    name = fields.Str()
    scope = fields.Str()
    project = fields.Str()


class SearchDatasetRequestSerializer(BaseSchema):
    __proto_class__ = SearchDatasetRequest
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    query = fields.Nested(DatasetFilterSerializer, missing={})
    page = fields.Int(missing=1)
    limit = fields.Int(missing=25)


class VersionFilterSerializer(Schema):
    id = fields.Str()
    name = fields.Str()
    dataset = fields.Str()
    author = fields.Str()


class SearchVersionRequestSerializer(BaseSchema):
    __proto_class__ = SearchVersionRequest
    __decode_options__ = {"preserving_proto_field_name": True,
                          "including_default_value_fields": False}

    query = fields.Nested(VersionFilterSerializer, missing={})
    page = fields.Int(missing=1)
    limit = fields.Int(missing=25)


class SearchDatasetResponseSerializer(BaseSchema):
    __proto_class__ = SearchDatasetResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(DatasetSerializer))


class SearchVersionResponseSerializer(BaseSchema):
    __proto_class__ = SearchVersionResponse

    total = fields.Int(default=0)
    page = fields.Int(default=1)
    limit = fields.Int(default=25)
    data = fields.List(fields.Nested(VersionSerializer))


dataset_serializer = DatasetSerializer()
version_serializer = VersionSerializer()
id_serializer = IDSerializer()
status_serializer = StatusSerializer()
search_dataset_request_serializer = SearchDatasetRequestSerializer()
search_version_request_serializer = SearchVersionRequestSerializer()
search_dataset_response_serializer = SearchDatasetResponseSerializer()
search_version_response_serializer = SearchVersionResponseSerializer()
