class Room:
    # list of sched_item

    def __init__(self, id, floor, max_capacity, schedule_item):
        self.id = id
        self.floor = floor
        self.maxCapacity = max_capacity
        self.schedule_item = schedule_item

    def print_floor(self):
        print "The room's floor is: ", self.floor

    def size_list_schedule_item(self):
        print len(self.schedule_item)
