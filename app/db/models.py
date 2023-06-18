from tortoise.models import Model
from tortoise import fields

from app.db import constants, validators


class Room(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False, unique=True)
    type = fields.CharEnumField(constants.RoomType)
    capacity = fields.IntField(validators=[validators.check_min_value(1, 'capacity')])
    status = fields.BooleanField(default=True)
    opens_at = fields.TimeField()
    closes_at = fields.TimeField()

    class Meta:
        table = 'room'

    def __str__(self):
        return self.name


class Resident(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField(null=True)

    class Meta:
        table = 'resident'

    def __str__(self):
        return self.name


class Booking(Model):
    id = fields.IntField(pk=True)
    room = fields.ForeignKeyField('models.Room', related_name='bookings')
    resident = fields.ForeignKeyField('models.Resident', related_name='bookings')
    start_time = fields.TimeField()
    end_time = fields.TimeField()
    date = fields.DateField()

    class Meta:
        table = 'booking'

    def __str__(self):
        return f'{self.resident.name} booked room {self.room.name}'
