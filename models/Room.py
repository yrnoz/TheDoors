from common.database import Database
from datetime import datetime

from models.Schedule import Schedule


def future_meeting(date):
    """

    :param date:
    :return: True if there is not a future meeting in this room
    """
    meeting_date = datetime.strptime(date, '%d/%m/%y')
    now = datetime.utcnow()
    if now < meeting_date:
        return False
    else:
        return True


"""
this class represent the rooms table in the DB
the format is like that:
 {'permission': 10 ,'company': google , 'facility': matam  , '_id': taub1 , 'capacity': 30, 'floor': 2 }

"""


class Room(object):
    def __init__(self, permission, capacity, _id, floor, company, facility):
        self.permission = permission
        self.capacity = capacity
        self._id = _id
        self.floor = floor
        self.company = company
        self.facility = facility

    def save_to_mongodb(self):
        Database.insert(collection='rooms', data=self.json())

    def json(self):
        return {
            'floor': self.floor,
            'capacity': self.capacity,
            '_id': self._id,
            'permission': self.permission,
            'company': self.company,
            'facility': self.facility
        }

    @classmethod
    def get_by_facility(cls, company, facility):
        data = Database.find('rooms', {'$and': [{'company': company}, {'facility': facility}]})
        rooms = []
        if data is not None:
            for room in data:
                rooms.append(cls(**room))
        return rooms

    @classmethod
    def get_by_company(cls, company):
        rooms = []
        data = Database.find('rooms', {'company': company})
        if data is not None:
            for room in data:
                rooms.append(cls(**room))
        return rooms

    @classmethod
    def get_by_capacity(cls, free_space, company, facility, permission):
        rooms = []
        print('free space:')
        print(type(free_space))
        query = {
            '$and':

                [
                    {
                        'company': company
                    },
                    {
                        'facility': facility
                    },
                    {
                        'permission':
                            {
                                '$not':
                                    {
                                        '$gt': permission
                                    }
                            }
                    },
                    {
                        'capacity':
                            {
                                '$gt': free_space
                            }
                    }
                ]

        }
        data = Database.find('rooms', query)
        if data is not None:
            for room in data:
                rooms.append(cls(**room))
        return rooms

    @classmethod
    def add_room(cls, permission, capacity, room_num, floor, company, facility):
        _id = company + " " + facility + ' ' + str(room_num)
        if not cls.is_room_exist(_id):
            new_room = cls(permission, capacity, _id, floor, company, facility)
            Database.insert('rooms', new_room.json())
            return True, _id
        else:
            # room already exist
            return False, _id

    @classmethod
    def is_room_exist(cls, _id):
        data = Room.get_by_id(_id)
        if data is None:
            return False
        else:
            return True

    @classmethod
    def remove_room(cls, _id):
        if not cls.is_room_exist(_id):
            return False
        else:
            room = Room.get_by_id(_id)
            room_schedule = room.get_schedules()
            for schedule in room_schedule:
                if future_meeting(schedule.date):
                    return False
            Database.remove('rooms', {'_id': _id})
            return True

    def get_schedules(self):
        return Schedule.get_by_room(self._id)

    @classmethod
    def available_rooms(cls, date, available_spaces, begin_meeting, end_meeting, permission, company, facility):
        """

        :param date:
        :param available_spaces:
        :param begin_meeting:
        :param end_meeting:
        :return: a list of all the room that have enough  space >= available_spaces  for a meeting on the given time
        """
        available_rooms = []

        rooms = Room.get_by_capacity(available_spaces, company, facility, permission)
        for room in rooms:
            if room.permission <= permission:
                room_schedule = Schedule.get_by_room_and_date(room._id, date)
                if len(room_schedule) > 0:
                    # this room already have some reservation
                    save_space = Schedule.saved_space(room_schedule, begin_meeting, end_meeting, available_spaces)
                    if room.capacity - save_space >= available_spaces:
                        available_rooms.append(cls(**room))
                else:
                    # this room is empty
                    available_rooms.append(cls(**room))
        return available_rooms

    @classmethod
    def company_rooms(cls, company, facility=None):
        """

        :param company:
        :param facility:
        :return: list of the rooms that belongs to this company,
        optional: if this function get facility it return the rooms of this company in this facility
        """
        rooms = []
        if facility is None:
            return Room.get_by_company(company)
        else:
            return Room.get_by_facility(company, facility)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('rooms', {'_id': _id})
        if data is not None:
            return cls(**data)
