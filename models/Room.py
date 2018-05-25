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
    def __init__(self, permission, capacity, _id, floor, company, facility, disabled_access):
        self.permission = permission
        self.capacity = capacity
        self._id = _id
        self.floor = floor
        self.company = company
        self.facility = facility
        self.disabled_access = disabled_access

    def save_to_mongodb(self):
        Database.insert(collection='rooms', data=self.json())

    def json(self):
        return {
            'floor': self.floor,
            'capacity': self.capacity,
            '_id': self._id,
            'permission': self.permission,
            'company': self.company,
            'facility': self.facility,
            'disabled_access': self.disabled_access
        }

    def intersection(self, start_time, end_time):
        if self.begin_meeting < start_time < self.end_meeting:
            return True
        elif self.begin_meeting < end_time < self.end_meeting:
            return True
        else:
            return False

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

    def available_on_time(self, date, start_time, end_time, demand_sits):
        schedules = self.get_schedules()
        save_place = 0
        for schedule in schedules:
            if schedule.date == date and self.intersection(start_time, end_time, ):
                save_place += 1
        return True if demand_sits < self.capacity - save_place else False

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
    def add_room(cls, permission, capacity, room_num, floor, company, facility, disabled_access=False):
        _id = company + " " + facility + ' ' + str(room_num)
        if not cls.is_room_exist(_id):
            print('not exist' + _id)
            new_room = cls(permission, capacity, _id, floor, company, facility, disabled_access)
            Database.insert('rooms', new_room.json())
            return True, _id
        else:
            print(' exist' + _id)

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
    def check_room_space(cls, min_occupancy, max_occupancy, room_capacity, current_capacity, available_spaces):
        percent_occupancy = (current_capacity + available_spaces) * 100 / room_capacity
        if room_capacity - current_capacity >= available_spaces and percent_occupancy >= min_occupancy and percent_occupancy <= max_occupancy:
            return True
        return False

    @classmethod
    def check_room_friends(cls, room_id, date, start_time, end_time, min_friends, max_friends):
        participants = Schedule.get_participants_by_room_date_and_hour(room_id, date, start_time, end_time)
        if len(participants) >= min_friends and len(participants) <= max_friends:
            return True
        return False

    @classmethod
    def check_accessible(cls, room_id, is_accessible):
        """

                :param room_id:
                :param is_accessible: does the room need to be accessible to disabled
                """
        room = Room.get_by_id(room_id)
        return is_accessible == False or room.disabled_access

    @classmethod
    def available_rooms(cls, date, available_spaces, begin_meeting, end_meeting, permission, company, facility,
                        min_occupancy, max_occupancy,
                        min_friends, max_friends, is_accessible):
        """

        :param date:
        :param available_spaces: the participent in the room
        :param begin_meeting:
        :param end_meeting:
        :return: a list of all the room that have enough  space >= available_spaces  for a meeting on the given time
        """
        available_rooms = []

        rooms = Room.get_by_capacity(available_spaces, company, facility, permission)
        for room in rooms:
            room_schedule = Schedule.get_by_room_and_date(room._id, date)
            if len(room_schedule) > 0:
                # this room already have some reservation
                save_space = Schedule.saved_space(room_schedule, begin_meeting, end_meeting)
                is_room_space_ok = cls.check_room_space(min_occupancy, max_occupancy, room.capacity, save_space,
                                                        available_spaces)
                # is_num_friends_ok = cls.check_room_friends(room._id, date, begin_meeting, end_meeting, min_friends,
                #                                            max_friends)
                # is_accessible_ok = cls.check_accessible(room._id, is_accessible)
                # if is_room_space_ok and is_num_friends_ok and is_accessible_ok:
                if is_room_space_ok:
                    available_rooms.append(room)
            else:
                # this room is empty
                available_rooms.append(room)
        return available_rooms

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('rooms', {'_id': _id})
        if data is not None:
            return cls(**data)
