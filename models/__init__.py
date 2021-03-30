# encoding: utf-8

from mongoengine import *
from config import MONGO_DATABASE_URL, MONGO_PASSWORD, MONGO_USER

connect(host=MONGO_DATABASE_URL, port=27017, username=MONGO_USER, password=MONGO_PASSWORD)
