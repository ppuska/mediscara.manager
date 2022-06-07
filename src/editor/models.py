import logging

from django.db import models

from .fiware.model import CollaborativeOrder

logger = logging.getLogger("django")


class CollaborativeModel(models.Model):

    incubator_type = models.TextField()
    production_count = models.IntegerField()
    creation_date = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"CollaborativeModel: {self.incubator_type=} {self.production_count=}"

    @classmethod
    def create_from_dataclass(cls, dataclass: CollaborativeOrder):
        obj = cls()
        obj.incubator_type = dataclass.incubator_type
        obj.production_count = dataclass.count
        obj.creation_date = dataclass.created
        obj.active = dataclass.active
        return obj
