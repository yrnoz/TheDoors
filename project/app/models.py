from flask_login import UserMixin
from mongoengine import *

from app import login


@login.user_loader
def load_user(id):
    return User.objects.get(user_id=str(id))


class Schedule(Document):
    room_id = StringField(max_length=50)
    date = DateTimeField()
    time = IntField()
    occupancy = IntField()
    employees_id = ListField(StringField(max_length=9))


class Room(Document):
    room_id = StringField(max_length=50, primary_key=True)
    floor = IntField()
    maxCapacity = IntField()
    # schedules = ListField(Nested(Schedule))
    schedules = ListField(Schedule)
    access_permission = IntField()


class User(UserMixin, Document):
    user_id = StringField(primary_key=True, max_length=9)
    username = StringField(required=True, unique=True)
    password = StringField(max_length=50)
    role = StringField(max_length=50)
    access_permission = IntField()
    friends = ListField(StringField(max_length=9))
    schedules = ListField(Schedule)
    location = StringField(max_length=50)

    def get_id(self):
        return self.user_id
