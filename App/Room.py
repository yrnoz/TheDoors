class Room:
    ## list of sched_item

    def __init__(self,ID, floor, maxCapacity, schedule_item):
        self.ID = ID
        self.floor = floor
        self.maxCapacity = maxCapacity
        self.schedule_item = schedule_item

    def printFloor(self):
        print "The room's floor is: " , self.floor

    def get_ID(self):
        return self.ID

    def get_floor(self):
        return self.floor

    def get_maxCapacity(self):
        return self.maxCapacity

    def size_list_schedule_item(self):
        print len(self.schedule_item)
