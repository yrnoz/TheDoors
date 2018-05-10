from common.database import Database
from models.Room import Room
from models.Schedule import Schedule
from datetime import datetime


class Order(object):
    def __init__(self, user_email, _id, date, participants, start_time, end_time, company,
                 facility, floor_constrain=None, friends_in_room=None, max_percent=None):

        _id = user_email + date + str(start_time) + str(end_time)
        self.user_email = user_email
        self.date = date
        self.participants = participants
        self.start_time = start_time
        self.end_time = end_time
        self.floor_constrain = floor_constrain
        self.friends_in_room = friends_in_room
        self.max_percent = max_percent
        self._id = _id
        self.company = company
        self.facility = facility

    def save_to_mongodb(self):
        Database.insert(collection='orders', data=self.json())

    def json(self):
        return {
            'user_email': self.user_email,
            'date': self.date,
            'participants': self.participants,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'floor_constrain': self.floor_constrain,
            'friends_in_room': self.friends_in_room,
            'max_percent': self.max_percent,
            '_id': self._id,
            'company': self.company,
            'facility': self.facility
        }

    def future_meeting(self):

        meeting_date = datetime.strptime(self.date, '%d/%m/%y')
        now = datetime.utcnow()
        if now < meeting_date:
            return False
        else:
            return True

    @classmethod
    def find_by_id(cls, order_id):
        data = Database.find('orders', {'_id': order_id})
        if data is not None:
            return cls(**data)

    @classmethod
    def find_by_user_email(cls, user_email):
        orders = []
        data = Database.find('orders', {'user_email': user_email})
        for order in data:
            orders.append(cls(**order))
        return orders

    @classmethod
    def find_by_user_email_and_date(cls, user_email, date):
        orders = []
        query = {'$and': [{'date': date}, {'user_email': user_email}]}
        data = Database.find('orders', query)
        for order in data:
            orders.append(cls(**order))
        return orders

    @classmethod
    def find_by_user_email_and_date_and_time(cls, user_email, date, beign, end):
        orders = []
        query = {
            '$and': [{'date': date}, {'user_email': user_email},
                     {'$or': [{'$gt': {'start_time': end}}, {'$st': {'end_time': beign}}]}]
        }
        data = Database.find('orders', query)
        for order in data:
            orders.append(cls(**order))
        return orders

    @classmethod
    def already_haev_an_order_on_this_time(cls, user_email, date, start_time, end_time):
        orders = cls.find_by_date_and_time(user_email, date, start_time, end_time)
        return True if len(orders) > 0 else False

    @classmethod
    def find_by_date_and_time(cls, user_email, date, beign, end):
        orders = []

        intersection = {
            '$or':
                [
                    {
                        '$and':
                            [
                                {
                                    'start_time':
                                        {
                                            '$not':
                                                {
                                                    '$gte': end

                                                }
                                        }

                                },
                                {
                                    'end_time':
                                        {
                                            '$gte': end
                                        }
                                }
                            ]
                    }
                    ,
                    {
                        '$and':
                            [
                                {
                                    'start_time':
                                        {
                                            '$not':
                                                {
                                                    '$gte': beign

                                                }
                                        }

                                },
                                {
                                    'end_time':
                                        {
                                            '$gt': beign
                                        }
                                }
                            ]
                    }
                ]
        }

        query = {
            '$and': [{'date': date}, {'user_email': user_email}, intersection]
        }
        data = Database.find('orders', query)
        for order in data:
            orders.append(cls(**order))
        return orders

    @classmethod
    def new_order(cls, user_email, date, participants, start_time, end_time, company, facility, min_permission,
                  floor_constrain=None, friends_in_room=None, max_percent=None):
        """

        :param user_email:
        :param date:
        :param participants:
        :param start_time:
        :param end_time:
        :param floor_constrain:
        :param friends_in_room:
        :param max_percent:
        :return: True if we can create new order:
        if this user_email already had an order on this time --> false
        if one of the participants already have a meeting on this time --> false
        else --> true
        """

        # user already have an order on that time
        if cls.already_haev_an_order_on_this_time(user_email, date, start_time, end_time):
            return False, "user already have an order on that time "

        if Schedule.all_participants_are_free(date, participants, start_time, end_time):
            new_order = cls(user_email, None, date, participants, start_time, end_time, floor_constrain,
                            friends_in_room, max_percent)
            # todo - schedule algorithm, after it run we know the room_id that we will assign them in.
            # todo - this algorithm try to assign the new order into specific room.
            # todo - if it can't do this then it start to chnage other orders.
            if new_order.try_schedule_naive_algorithm(company, facility, min_permission):
                new_order.save_to_mongodb()
                return True, new_order._id
            else:
                return False, "failed"
        return False, " problem with some participants"

    @classmethod
    def participant_cancel(cls, user_email, order_id):
        """
        remove user_email from the participants list of this order and save it to db
        :param user_email:
        :param order_id:
        """
        order = Database.find_one('orders', {'_id': order_id})
        if order is not None:
            order = cls(**order)
            Database.remove('orders', {'_id': order_id})
            order.participants.remove(user_email)
            Database.insert('orders', order.json())

    @classmethod
    def delete_order(cls, order_id):
        Database.remove('orders', {'_id': order_id})

    @classmethod
    def who_create_order(cls, order_id):
        order = cls.find_by_id(order_id)
        return order.user_email

    def try_schedule_naive_algorithm(self, company, facility, min_permission):
        orders = Order.find_by_facility(company, facility)
        rooms = Room.available_rooms(self.date, len(self.participants), self.start_time, self.end_time, min_permission,
                                     company, facility)
        result = {}
        for room in rooms:
            if room.avialable_on_time(self.date, self.start_time, self.end_time):
                return self._id, room._id

    @classmethod
    def find_by_facility(cls, company, facility):
        orders = []
        data = Database.find('orders', {'$and': [{'company': company}, {'facility': facility}]})
        if data is not None:
            for order in data:
                orders.append(cls(**order))
        return orders

    def remove_participant(self, user_email):
        self.participants.remove(user_email)
        Database.update('orders', {'email': user_email}, self.json())

    @classmethod
    def get_orders_by_participant(cls, user_email):
        orders = []
        data = Database.find('orders', {'participants': {'$in': [user_email]}})
        if data is not None:
            for order in data:
                orders.append(cls(**order))
        return orders

    @staticmethod
    def remove_user(user_email):
        orders = Order.find_by_user_email(user_email)
        orders = [order for order in orders if order.future_meeting()]
        if len(orders) > 0:
            return False
        else:
            orders = Order.get_orders_by_participant(user_email)
            orders = [order for order in orders if order.future_meeting()]
            for order in orders:
                order.remove_participant(user_email)
            return True
