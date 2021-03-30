# encoding: utf-8
from bson import ObjectId


def increment_version(version: str):
    current_id = int(version.replace('.', ''))
    return '.'.join(list(str(current_id + 1)))


def construct_mongo_query(data: dict, mappings: dict, ids: list):
    query = {}
    for key, value in data.items():
        if value and key in mappings.keys():
            query[mappings[key]] = value

    for key in query.keys():
        if key in ids:
            query[key] = ObjectId(query[key])
    return query
