# encoding: utf-8
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
