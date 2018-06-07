"""
This class represent the weekly schedule for user.
if a user want to order room,
 first we check if on this time the user already have a meeting .

 the schedule  is a dictionary that looks ike that:
{'date': 12/11/23 , 'email': user@email.com, 'room_id': taub1, 'begin_meeting': 8 , 'end_meeting': 10 , 'order_id': the order id}

 order id - that we can find all the participants in this meeting
"""
from common.database import Database
from datetime import datetime

time_dict = {'8': "08:00", '9': "09:00", '10': "10:00", '11': "11:00", '12': "12:00", '13': "13:00", '14': "14:00",
             '15': "15:00", '16': "16:00", "17": "17:00", '18': "18:00"}


class Schedule(object):

    def __init__(self, email, date, begin_meeting, end_meeting, order_id, participants, room_id=None, _id=None):
        _id = email + ' ' + date + ' ' + room_id + ' start: ' + str(begin_meeting) + ' end: ' + str(end_meeting)
        self.email = email
        self._id = _id
        self.date = date
        self.room_id = room_id
        self.order_id = order_id
        self.begin_meeting = begin_meeting
        self.end_meeting = end_meeting
        self.participants = participants

    def save_to_mongodb(self):
        data = self.json()
        print(data)
        data1 = Database.find_one('schedules' , {'email': 'email_1@gmail.com'})
        data2 = Database.find_one('schedules', {'email': 'email_4@gmail.com'})
        Database.insert(collection='schedules', data=self.json())

    def save_to_mongodb_simulation(self):
        data = self.json()
        print(data)
        data1 = Database.find_oneSimulation('schedules' , {'email': 'email_1@gmail.com'})
        data2 = Database.find_oneSimulation('schedules', {'email': 'email_4@gmail.com'})
        Database.insertSimulation(collection='schedules', data=self.json())

    def json(self):
        return {
            'email': self.email,
            '_id': self._id,
            'date': self.date,
            'room_id': self.room_id,
            'order_id': self.order_id,
            'begin_meeting': self.begin_meeting,
            'end_meeting': self.end_meeting,
            'participants': self.participants,
        }

    def future_meeting(self):
        meeting_date = datetime.strptime(self.date, '%d/%m/%y')
        now = datetime.utcnow()
        if now < meeting_date:
            return False
        else:
            return True

    def get_start_time(self):
        """
            :return the time in this format: "10:30"
        """
        return time_dict[str(self.begin_meeting)]

    def get_end_time(self):
        return time_dict[str(self.end_meeting)]

    @classmethod
    def remove_user(cls, user_email):
        schedules = Schedule.get_schedules(user_email)
        schedules = [sched for sched in schedules if sched.future_meeting()]
        for sched in schedules:
            Database.remove('schedules', {'email': sched.email})

    @classmethod
    def get_schedules(cls, user_email, date=None, start_time=None, end_time=None, room_id=None):
        """

        :return: list of schedule's object that represent the schedule of the user's email
        """
        email_query = {'email': user_email}
        date_query = {'date': date} if date is not None else {}
        room_query = {'room_id': room_id} if room_id is not None else {}
        begin_query = {'begin_meeting': start_time} if start_time is not None else {}
        end_query = {'end_meeting': end_time} if end_time is not None else {}
        #query = {'$and': [email_query, date_query, room_query, begin_query, end_query]}
        query ={'email': user_email}
        schedules = []
        data = Database.find('schedules', query)
        print(query)
        print(date)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_schedules_simulation(cls, user_email, date=None, start_time=None, end_time=None, room_id=None):
        """

        :return: list of schedule's object that represent the schedule of the user's email
        """
        email_query = {'email': user_email}
        date_query = {'date': date} if date is not None else {}
        room_query = {'room_id': room_id} if room_id is not None else {}
        begin_query = {'begin_meeting': start_time} if start_time is not None else {}
        end_query = {'end_meeting': end_time} if end_time is not None else {}
        # query = {'$and': [email_query, date_query, room_query, begin_query, end_query]}
        query = {'email': user_email}
        schedules = []
        data = Database.findSimulation('schedules', query)
        print(query)
        print(date)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    def get_day(self):
        date = datetime.strptime(self.date, '%d/%m/%y')
        return str(date.strftime("%A"))

    @classmethod
    def get_by_room(cls, room_id):
        """

        :param room_id:
        :return: list of schedule's object that represent the schedule in the given room_id
        """
        schedules = []
        data = Database.find('schedules', {'room_id': room_id})
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_room_simulation(cls, room_id):
        """

        :param room_id:
        :return: list of schedule's object that represent the schedule in the given room_id
        """
        schedules = []
        data = Database.findSimulation('schedules', {'room_id': room_id})
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules


    @classmethod
    def all_participants_are_free(cls, date, participants, start_time, end_time):
        problematics = []
        for user_email in participants:
            data = cls.get_schedules(user_email, date)
            print(data)
            print('that wa daatatat')
            for sched in data:
                # this user is not free on this time
                print(sched._id)
                if not sched.is_available(start_time, end_time):
                    problematics.append(user_email)
                    break
        return problematics

    @classmethod
    def all_participants_are_free_simulation(cls, date, participants, start_time, end_time):
        problematics = []
        for user_email in participants:
            data = cls.get_schedules_simulation(user_email, date)
            print(data)
            print('that wa daatatat')
            for sched in data:
                # this user is not free on this time
                print(sched._id)
                if not sched.is_available(start_time, end_time):
                    problematics.append(user_email)
                    break
        return problematics

    @classmethod
    def delete_meeting_from_schedule(cls, date, participants, start_time, end_time):
        """
         delete the meeting from the schedule of every user in the participants list.
        :param date: the date of the meeting
        :param participants: the emails of the peoples that invited to this meeting
        :param start_time:
        :param end_time:
        """

        for user_email in participants:
            # check that all the participants really have a meeting on this time
            schedule = Schedule.get_by_email_and_date_and_hour(user_email, date, start_time, end_time)
            if schedule is None:
                return False
        for user_email in participants:
            schedules = Schedule.get_by_email_and_date_and_hour(user_email, date, start_time, end_time)
            for sched in schedules:
                schedule_id = cls.get_sched_id(sched)
                Database.remove('schedules', {'_id': schedule_id})
        return True

    @classmethod
    def delete_meeting_from_schedule_simulation(cls, date, participants, start_time, end_time):
        """
         delete the meeting from the schedule of every user in the participants list.
        :param date: the date of the meeting
        :param participants: the emails of the peoples that invited to this meeting
        :param start_time:
        :param end_time:
        """

        for user_email in participants:
            # check that all the participants really have a meeting on this time
            schedule = Schedule.get_by_email_and_date_and_hour_simulation(user_email, date, start_time, end_time)
            if schedule is None:
                return False
        for user_email in participants:
            schedules = Schedule.get_by_email_and_date_and_hour_simulation(user_email, date, start_time, end_time)
            for sched in schedules:
                schedule_id = cls.get_sched_id(sched)
                Database.removeSimulation('schedules', {'_id': schedule_id})
        return True

    def is_available(self, start_time, end_time):
        """

        :param start_time:
        :param end_time:
        :return: True if [start_time,end_time] intersection with [ self.begin_meeting , self.end_meeting] is empty
        """
        before = (int(end_time) <= int(self.begin_meeting))
        after = (int(start_time) >= int(self.end_meeting))
        return True if (before or after) else False

    #simulation
    @classmethod
    def assign_all(cls, date, participants, start_time, end_time, order_id, room_id):
        for user_email in participants:
            new_meeting = Schedule(user_email, date, start_time, end_time, order_id, participants, room_id)
            sched_user =cls.get_by_email_and_date_and_hour(user_email, date, start_time, end_time)
            if len(sched_user)==0:
                new_meeting.save_to_mongodb()

    @classmethod
    def assign_all_simulation(cls, date, participants, start_time, end_time, order_id, room_id):
        for user_email in participants:
            new_meeting = Schedule(user_email, date, start_time, end_time, order_id, participants, room_id)
            sched_user = cls.get_by_email_and_date_and_hour_simulation(user_email, date, start_time, end_time) #simulation
            if len(sched_user) == 0:
                new_meeting.save_to_mongodb_simulation()

    @classmethod
    def saved_space(cls, room_schedule, begin_meeting, end_meeting):
        """
        :return the number of the save spaces during the given time
        """
        save_place = 0
        for schedule in room_schedule:
            if not schedule.is_available(begin_meeting, end_meeting):
                # there is a meeting on the the given time, so save_place++
                save_place += schedule.participants
        return save_place

    @classmethod
    def get_by_id(cls, _id):
        """
             :return: list of schedule's object that represent the schedule in the given room_id on the given date
             """
        query = {'_id': _id}
        data = Database.find_one('schedules', query)
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_order(cls, order_id):
        all_scheds = []
        query = {'order_id': order_id}
        data = Database.find('schedules', query)

        if data is not None:
            for sched in data:
                all_scheds.append(cls(**sched))
        return all_scheds

    @classmethod
    def get_by_order_simulation(cls, order_id):
        all_scheds = []
        query = {'order_id': order_id}
        data = Database.findSimulation('schedules', query)

        if data is not None:
            for sched in data:
                all_scheds.append(cls(**sched))
        return all_scheds

    @classmethod
    def get_by_room_and_date(cls, _id, date):
        """
             :return: list of schedule's object that represent the schedule in the given room_id on the given date
             """
        schedules = []
        query = {'$and': [{'date': date}, {'room_id': _id}]}
        data = Database.find('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_room_and_date_simulation(cls, _id, date):
        """
             :return: list of schedule's object that represent the schedule in the given room_id on the given date
             """
        schedules = []
        query = {'$and': [{'date': date}, {'room_id': _id}]}
        data = Database.findSimulation('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_room_and_date_and_hour(cls, _id, date, begin_hour, end_hour):
        schedules = []
        query = {'$and': [{'date': date}, {'room_id': _id},
                          {'$or': [{'$gt': {'start_time': end_hour}}, {'$st': {'end_time': begin_hour}}]}]}
        data = Database.find('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_email_and_date_and_hour(cls, email, date, begin_hour, end_hour):
        ###need to change the queary
        schedules = []
        query = {'$and': [{'date': date}, {'email':email}, {'begin_meeting': begin_hour}, {'end_meeting': end_hour}]}
        #query = {'$and': [{'date': date}, {'email': email},
         #                 {'$or': [{'$gt': {'begin_meeting': end_hour}}, {'$st': {'end_meeting': begin_hour}}]}]}
        data = Database.find('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_email_and_date_and_hour_simulation(cls, email, date, begin_hour, end_hour):
        ###need to change the queary
        schedules = []
        query = {'$and': [{'date': date}, {'email': email}, {'begin_meeting': begin_hour}, {'end_meeting': end_hour}]}
        # query = {'$and': [{'date': date}, {'email': email},
        #                 {'$or': [{'$gt': {'begin_meeting': end_hour}}, {'$st': {'end_meeting': begin_hour}}]}]}
        data = Database.findSimulation('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_date_and_hour(cls, date, begin_hour, end_hour):
        schedules = []
        query ={'$and': [{'date': date}, {'begin_meeting': begin_hour}]}
        #query = {'$and': [{'date': date},
         #                 {'$or': [{'$gt': {'begin_meeting': end_hour}}, {'$st': {'end_meeting': begin_hour}}]}]}
        data = Database.find('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_date_and_hour_simulation(cls, date, begin_hour, end_hour):
        schedules = []
        query = {'$and': [{'date': date}, {'begin_meeting': begin_hour}]}
        # query = {'$and': [{'date': date},
        #                 {'$or': [{'$gt': {'begin_meeting': end_hour}}, {'$st': {'end_meeting': begin_hour}}]}]}
        data = Database.findSimulation('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_participants_by_room_date_and_hour(cls, _id, date, start_time, end_time):
        schedule = Schedule.get_by_room_and_date_and_hour(date, start_time, end_time)
        return schedule.participants

    @classmethod
    def get_sched_id(cls, sched):
        return sched._id

    @classmethod
    def get_participants(cls, sched):
        return sched.participants

    @classmethod
    def cancel_meeting(cls, meeting_id):
        data = Database.find_one('schedules', {'_id': meeting_id})
        if data is not None:
            data = cls(**data)
            Database.remove('schedules', {'_id': meeting_id})
            return data.order_id

    @classmethod
    def delete_order(cls, order_id):
        Database.remove('schedules', {'order_id': order_id})
