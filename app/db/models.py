from tortoise.models import Model
from tortoise import fields

from app.db import constants, validators


class Room(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False, unique=True)
    type = fields.CharEnumField(constants.RoomType)

    class Meta:
        table = 'room'

    def __str__(self):
        return self.name


class Resident(Model):
    name = fields.CharField(max_length=100, null=False, unique=True)
    email = fields.CharField(max_length=100, unique=True, validators=[validators.validate_email])
    start_date = fields.DateField()
    end_data = fields.DateField()

    class Meta:
        table = 'resident'

    def __str__(self):
        return self.name


class Booking(Model):
    id = fields.IntField(pk=True)
    room = fields.ForeignKeyField('Room', related_name='bookings')
    resident = fields.ForeignKeyField('Resident', related_name='bookings')
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()

    class Meta:
        table = 'booking'

    def __str__(self):
        return f'{self.resident.name} booked room {self.room.name}'
