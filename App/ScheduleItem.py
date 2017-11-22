class ScheduleItem:
    def __init__(self, date_time, occupancy, max_occupancy=None):
        self.date_time = date_time
        self.occupancy = occupancy
        self.max_occupancy = max_occupancy  # if no constraint is made, max_occupancy is None
