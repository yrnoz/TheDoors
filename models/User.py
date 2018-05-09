from datetime import datetime

from models.Room import Room
from models.Schedule import Schedule
from models.Order import Order
from flask import session

from common.database import Database
from models.facilities import Facilities
from models.friends import Friends


class User(object):
    def __init__(self, email, username, password, _id, role, permission, company, facility,
                 added_date=datetime.utcnow().strftime('%d/%m/%y')):
        self.email = email
        self.password = password
        self.username = username
        self._id = _id
        self.role = role
        self.permission = permission
        self.company = company
        self.facility = facility
        self.added_date = added_date

    def save_to_mongodb(self):
        Database.insert(collection='users', data=self.json())

    def json(self):
        return {
            'email': self.email,
            'username': self.username,
            'password': self.password,
            '_id': self._id,
            'role': self.role,
            'permission': self.permission,
            'company': self.company,
            'facility': self.facility,
            'added_date': self.added_date,
        }

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one('users', {'email': email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # Check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password
            return user.password == password
        return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_friends(self):
        return Friends.get_friends(self.email)

    def add_friend(self, friend_email):
        friend = User.get_by_email(friend_email)
        if friend is not None:
            if friend.company == self.company:
                return Friends.add_friend(self.email, friend_email)
            return False, "not in the same company, sorry"
        return False, "email dose'nt exist"

    def create_meeting(self, start_time, end_time, order_id, room_id, date=datetime.utcnow().strftime('%d/%m/%y'),
                       participants=[]):
        if self.email not in participants:
            participants.append(self.email)
        Schedule.add_meeting_to_schedule(date, participants, start_time, end_time, order_id, room_id)

    def remove_friend(self, friend_email):
        return Friends.remove_friend(self.email, friend_email)

    def get_orders(self, start=None, end=None):
        # todo
        return Order.find_by_id(self._id)

    def get_schedule(self, start=None, end=None):
        # todo
        return Schedule.get_by_email(self.email, start, end)

    def new_order(self, date, participants, start_time, end_time, company, facility, floor_constrain=None,
                  friends_in_room=None, max_percent=None):
        # todo fix this function
        if self.email not in participants:
            participants.append(self.email)

        min_permission = User.min_permission(participants)

        status, order_id = Order.new_order(self.email, date, participants, start_time, end_time, company, facility,
                                           min_permission, floor_constrain, friends_in_room, max_percent)
        user = User.get_by_email(self.email)
        if status:
            rooms = Room.available_rooms(date, len(participants), start_time, end_time, min_permission, user.company,
                                         user.facility)
            print(rooms)
            for user in participants:
                user = User.get_by_email(user)
                if user is not None:
                    user.create_meeting(start_time, end_time, order_id, date, participants)

    def cancel_meeting(self, meeting_id):
        """
        this user won't come to this meeting so the user decide to cancel it
        :param meeting_id:
        """

        order_id = Schedule.cancel_meeting(meeting_id)
        if Order.who_create_order(order_id) == self.email:
            return self.cancel_order(order_id)
        if order_id is not None:
            Order.participant_cancel(self.email, order_id)

    def cancel_order(self, order_id):
        """
        this method delete the order that match this order_id from the 'orders' table in db
        and delete the meeting from the schedule of each participant that invited to this meeting.
        only the user taht create this order can cancel it
        :param order_id:
        """
        if Order.who_create_order(order_id) == self.email:
            Order.delete_order(order_id)
            Schedule.delete_order(order_id)

    @classmethod
    def min_permission(cls, participants):
        permission = 1000000000
        for user in participants:
            user = User.get_by_email(user)
            if user is not None:
                permission = user.permission if user.permission < permission else permission
        return permission


class Manager(User):

    @classmethod
    def manager_register(cls, email, password, username, _id, role, permission, company, facility):
        data = Database.find_one('facilities', {'company': company})
        if data is not None:
            return False, "company already exist"
        else:
            Facilities.add_company(company, facility)
            user = cls.get_by_email(email)
            if not cls.check_id(_id):
                return False, "bad number ID"
            if user is None:
                # User dose'nt exist, create new user
                new_user = cls(email, password, username, _id, role, permission, company, facility)
                try:
                    new_user.save_to_mongodb()
                    session['email'] = email
                    return True
                except Exception as e:
                    return False, str(e)
            else:
                # User already exist
                return False, "user email already exist"

    @classmethod
    def check_id(cls, _id):
        """check if the given _id is legal id"""
        if len(str(_id)) != 9:
            return False
        sum = 0
        factor = 0
        for i in _id:
            tmp = int(i) * (factor + 1)
            factor = (factor + 1) % 2
            dig = 1 if tmp > 9 else 0
            sum += tmp % 10 + dig
        return False if sum % 10 != 0 else True

    @classmethod
    def user_register(cls, email, password, username, _id, role, permission, company, facility):
        if not Facilities.is_company_exist(company):
            return False, "company dose'nt exist"
        user = cls.get_by_email(email)
        if not cls.check_id(_id):
            return False, "bad number ID"
        if user is None:
            # User dose'nt exist, create new user
            new_user = cls(email, password, username, _id, role, permission, company, facility)
            try:
                new_user.save_to_mongodb()
            except Exception as e:
                return False, str(e)
            return True
        else:
            # User already exist
            return False, "user email already exist"

    def delete_user(self, user_email):
        user = User.get_by_email(user_email)
        if user is not None and user.company == self.company:
            if Order.remove_user(user_email):
                Friends.remove_user(user_email)
                Schedule.remove_user(user_email)
                Database.DATABASE.remove('users', {'email': user_email})
                return True
        return False
