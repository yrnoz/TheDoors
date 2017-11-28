class RoomOrder:

    def _init_ (self, date_time, num_participents):
        self.date_time = date_time
        self.num_participents = num_participents

    def get_numParticpents(self):
        return self.num_participents
