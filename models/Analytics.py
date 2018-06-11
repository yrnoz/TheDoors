from common.database import Database

"""
    in this class we implement tools for the analytics
    
"""


class Analytics(object):

    @staticmethod
    def get_room_occupancy(room_id, facility_id, time):
        query = {'$and': [{'facility': facility_id}, {'room': room_id}]}
        room = Database.find_one('rooms', query)
        if room is None:
            return
        # TODO: implement get_occupancy (will be after room ordering is done)
        occupancy = room.get_occupancy(time)
        return occupancy/room.capacity

    @staticmethod
    def get_room_occupancy_simulation(room_id, facility_id, time):
        query = {'$and': [{'facility': facility_id}, {'room': room_id}]}
        room = Database.find_oneSimulation('rooms', query)
        if room is None:
            return
        # TODO: implement get_occupancy (will be after room ordering is done)
        occupancy = room.get_occupancy_simulation(time)
        return occupancy / room.capacity

    @staticmethod
    def get_num_employees_company(company_id):
        query = {'company_id': company_id}
        emps = Database.find('users', query)
        if emps is None:
            return
        return emps.count(True)

    @staticmethod
    def get_num_employees_company_simulation(company_id):
        query = {'company_id': company_id}
        emps = Database.findSimulation('users', query)
        if emps is None:
            return
        return emps.count(True)

    @staticmethod
    def get_num_employees_facility(company_id, facility_id):
        query = {'$and': [{'facility': facility_id}, {'company_id': company_id}]}
        emps = Database.find('users', query)
        if emps is None:
            return
        return emps.count(True)

    @staticmethod
    def get_num_employees_facility_simulation(company_id, facility_id):
        query = {'$and': [{'facility': facility_id}, {'company_id': company_id}]}
        emps = Database.findSimulation('users', query)
        if emps is None:
            return
        return emps.count(True)

    @staticmethod
    def get_num_rooms_facility(company_id):
        query = {'company_id': company_id}
        rooms = Database.find('rooms', query)
        if rooms is None:
            return
        return rooms.count(True)

    @staticmethod
    def get_num_rooms_facility_simulation(company_id):
        query = {'company_id': company_id}
        rooms = Database.findSimulation('rooms', query)
        if rooms is None:
            return
        return rooms.count(True)

    @staticmethod
    def get_num_rooms_facility(company_id, facility_id):
        query = {'$and': [{'facility': facility_id}, {'company_id': company_id}]}
        rooms = Database.find('rooms', query)
        if rooms is None:
            return
        return rooms.count(True)

    @staticmethod
    def get_num_rooms_facility_simulation(company_id, facility_id):
        query = {'$and': [{'facility': facility_id}, {'company_id': company_id}]}
        rooms = Database.findSimulation('rooms', query)
        if rooms is None:
            return
        return rooms.count(True)
