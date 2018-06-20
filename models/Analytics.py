import functools

from common.database import Database
from datetime import datetime, timedelta

from models.Schedule import Schedule
from models.Room import Room

"""
    in this class we implement tools for the analytics

"""


class Analytics(object):
    @staticmethod
    def get_meetings_number_in_facility(manager, facility_name):
        rooms = Room.get_by_facility(manager.company, facility_name)
        if rooms is None:
            return
        sum_meetings = 0
        for room in rooms:
            occupancy = room.get_occupancy(datetime.now(), room._id)
            sum_meetings += occupancy
        return sum_meetings

    @staticmethod
    def get_all_participants_in_facility(manager, facility_name):
        rooms = Room.get_by_facility(manager.company, facility_name)
        if rooms is None:
            return
        sum_visits = 0
        for room in rooms:
            schedules = Schedule.get_by_room_and_date(room._id, datetime.now().strftime('%d/%m/%Y'))
            for sched in schedules:
                sum_visits += len(sched.participants)
        return sum_visits

    @staticmethod
    def get_meeting_number(manager):
        all_rooms = Room.get_by_company(manager.company)
        if all_rooms is None:
            return
        meetings = []
        for room in all_rooms:
            occupancy = room.get_occupancy(datetime.now(), room._id)
            meetings.append(occupancy)
        return functools.reduce(lambda a, b: a + b, meetings)

    @staticmethod
    def get_all_rooms_occupancy(manager):
        all_rooms = Room.get_by_company(manager.company)
        if all_rooms is None:
            return
        occupancies = []
        for room in all_rooms:
            occupancy = room.get_occupancy(datetime.now(), room._id)
            occupancies.append((room._id, occupancy / room.capacity))
        return occupancies

    @staticmethod
    def get_room_occupancy(room_id, facility_id, time=datetime.now()):
        query = {'$and': [{'facility': facility_id}, {'room': room_id}]}
        room = Database.find_one('rooms', query)
        if room is None:
            return
        occupancy = room.get_occupancy(time, room_id)
        return occupancy / room.capacity

    @staticmethod
    def get_room_occupancy_simulation(room_id, facility_id, time):
        query = {'$and': [{'facility': facility_id}, {'room': room_id}]}
        room = Database.find_oneSimulation('rooms', query)
        if room is None:
            return
        occupancy = room.get_occupancy_simulation(time)
        return occupancy / room.capacity

    @staticmethod
    def get_num_rooms_facility(company_id, facility_id=None):
        if facility_id is None:
            query = {'company': company_id}
            # print "Here"
        else:
            query = {'$and': [{'facility': facility_id}, {'company': company_id}]}
            # print query
        rooms = Database.find('rooms', query)
        if rooms is None:
            return
        return rooms.count(True)

    @staticmethod
    def get_num_rooms_facility_simulation(company_id, facility_id=None):
        if facility_id is None:
            query = {'company': company_id}
        else:
            query = {'$and': [{'facility': facility_id}, {'company': company_id}]}
        rooms = Database.findSimulation('rooms', query)
        if rooms is None:
            return
        return rooms.count(True)

    @staticmethod
    def get_num_employees_facility(company_id, facility_id=None):
        if facility_id is None:
            query = {'company': company_id}
        else:
            query = {'$and': [{'facility': facility_id}, {'company': company_id}]}
        emps = Database.find('users', query)
        if emps is None:
            return
        return emps.count(True)

    @staticmethod
    def get_num_employees_facility_simulation(company_id, facility_id=None):
        if facility_id is None:
            query = {'company': company_id}
        else:
            query = {'$and': [{'facility': facility_id}, {'company': company_id}]}
        emps = Database.findSimulation('users', query)
        if emps is None:
            return
        return emps.count(True)

