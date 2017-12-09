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
        update_room(self.id, self.floor, self.maxCapacity, self.access_permission , self.schedule)
