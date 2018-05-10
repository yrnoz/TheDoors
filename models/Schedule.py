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


class Schedule(object):

    def __init__(self, email, date, begin_meeting, end_meeting, order_id, room_id=None, _id=None):
        _id = email + date + room_id + ' start: ' + str(begin_meeting) + ' end: ' + str(end_meeting)
        self.email = email
        self._id = _id
        self.date = date
        self.room_id = room_id
        self.order_id = order_id
        self.begin_meeting = begin_meeting
        self.end_meeting = end_meeting

    def save_to_mongodb(self):
        Database.insert(collection='schedules', data=self.json())

    def json(self):
        return {
            'email': self.email,
            '_id': self._id,
            'date': self.date,
            'room_id': self.room_id,
            'order_id': self.order_id,
            'begin_meeting': self.begin_meeting,
            'end_meeting': self.end_meeting,

        }

    @classmethod
    def get_by_email_and_date_and_room(cls, email, date, room_id):
        """

        :param email:
        :param date:
        :param room_id:

        :return: list of schedule's object that represent the schedule of the user's email on the given date
            in the given room_id
        """
        schedules = []
        query = {'$and': [{'email': email}, {'date': date}, {'room_id': room_id}]}
        data = Database.find('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_email_and_date(cls, email, date):
        """

        :param email:
        :param date:
        :return: list of schedule's object that represent the schedule of the user's email on the given date
        """
        schedules = []
        query = {'$and': [{'email': email}, {'date': date}]}

        data = Database.find('schedules', query)
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    def future_meeting(self):
        meeting_date = datetime.strptime(self.date, '%d/%m/%y')
        now = datetime.utcnow()
        if now < meeting_date:
            return False
        else:
            return True

    @classmethod
    def remove_user(cls, user_email):
        schedules = Schedule.get_by_email(user_email)
        schedules = [sched for sched in schedules if sched.future_meeting()]
        for sched in schedules:
            Database.remove('schedules', {'email': sched.email})

    @classmethod
    def get_by_email(cls, email, start=None, end=None):
        """

        :param email:
        :return: list of schedule's object that represent the schedule of the user's email
        """
        schedules = []
        data = Database.find('schedules', {'email': email})
        if data is not None:
            for sched in data:
                schedules.append(cls(**sched))
        return schedules

    @classmethod
    def get_by_start_time(cls, user_email, date, start_time, end_time):
        """
       :return:  object that represent the schedule of the user's email on the given date
       on the given time
        """

        query = {
            '$and': [{'email': user_email}, {'date': date}, {'begin_meeting': start_time}, {'end_meeting': end_time}]
        }

        data = Database.find_one('schedules', query)
        if data is not None:
            return cls(**data)

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
    def all_participants_are_free(cls, date, participants, start_time, end_time):
        for user_email in participants:
            data = cls.get_by_start_time(user_email, date, start_time, end_time)
            if data is not None:
                # this user is not free on this time
                return False
        return True


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
            schedule = Schedule.get_by_start_time(user_email, date, start_time, end_time)
            if schedule is None:
                return False
        for user_email in participants:
            schedule = Schedule.get_by_start_time(user_email, date, start_time, end_time)
            Database.remove('schedules', {'_id': schedule._id})
        return True

    def is_available(self, start_time, end_time):
        """

        :param start_time:
        :param end_time:
        :return: True if [start_time,end_time] intersection with [ self.begin_meeting , self.end_meeting] is empty
        """
        before = (end_time <= self.begin_meeting)
        after = (start_time >= self.end_meeting)
        return True if (before or after) else False

    @classmethod
    def assign_all(cls, date, participants, start_time, end_time, order_id, room_id):
        participants = set(participants)
        for user_email in participants:
            new_meeting = Schedule(user_email, date, start_time, end_time, order_id, room_id)
            new_meeting.save_to_mongodb()

    @classmethod
    def saved_space(cls, room_schedule, begin_meeting, end_meeting):
        """
        :return the number of the save spaces during the given time
        """
        save_place = 0
        for schedule in room_schedule:
            if not schedule.is_available(begin_meeting, end_meeting):
                # there is a meeting on the the given time, so save_place++
                save_place += 1
        return save_place

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

    def get_order_id(self):
        return self.order_id

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
