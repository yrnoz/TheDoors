from datetime import datetime

from Database.ManageDB import update_room


class Room:
    # list of sched_item

    def __init__(self, id, floor, max_capacity, access_permission):
        self.id = id
        self.floor = floor
        self.maxCapacity = max_capacity
        self.schedule = {}
        self.access_permission = access_permission

    def print_floor(self):
        print "The room's floor is: ", self.floor

    def size_list_schedule(self):
        print len(self.schedule)

    def change_permission(self, access_permission):
        self.access_permission = access_permission

    def get_permission(self):
        return self.access_permission

    def add_schedule(self, schedule):
        self.schedule.update(schedule)
        update_room(self.id, self.floor, self.maxCapacity, self.access_permission, self.schedule)

    def get_capacity(self, date_time=datetime.now().strftime("%d/%m/%y %H")):
        return self.schedule.get(date_time, (0, 0))[1]

    def free_place(self, occupancy=1, date_time=datetime.now().strftime("%d/%m/%y %H")):
        """
        :param occupancy: the amount we want to make sure that we have place for them
        :param date_time: the time we want to enter the room
        :return:  true if there is enough place in the room else false
        """
        return occupancy <= self.maxCapacity - self.get_capacity(date_time)
