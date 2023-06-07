from tortoise.models import Model
from tortoise import fields


class Room(Model):
    name = fields.CharField(max_length=100, null=False, unique=True)

    class Meta:
        table = 'room'


class Resident(Model):
    name = fields.CharField(max_length=100, null=False, unique=True)

    class Meta:
        table = 'resident'
