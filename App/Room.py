class Room:
    # list of sched_item

    def __init__(self, id, floor, max_capacity):
        self.id = id
        self.floor = floor
        self.maxCapacity = max_capacity
        self.schedule = {}

    def print_floor(self):
        print "The room's floor is: ", self.floor

    def size_list_schedule(self):
        print len(self.schedule)

