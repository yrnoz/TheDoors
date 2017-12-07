class ScheduleItem:
    def __init__(self, date_time, occupancy, max_occupancy=None):
        self.date_time = date_time
        self.occupancy = occupancy
        self.max_occupancy = max_occupancy  # if no constraint is made, max_occupancy is None

    def to_tuple(self):
        return self.date_time, self.occupancy, self.max_occupancy

    @staticmethod
    def from_tuple(tup):
        if len(tup) == 3:
            return ScheduleItem(tup[0], tup[1], tup[2])
        if len(tup) == 2:
            return ScheduleItem(tup[0], tup[1])