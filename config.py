# coding: utf-8

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
