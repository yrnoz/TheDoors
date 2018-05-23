from common.database import Database
from models.Room import Room
from models.Schedule import Schedule
from datetime import datetime


class Order(object):
    def __init__(self, user_email, _id, date, participants, start_time, end_time, company,
                 facility, min_occupancy, max_occupancy, min_friends, max_friends, is_accessible):

        #_id = user_email + date + str(start_time) + str(end_time)
        self.user_email = user_email
        self.date = date
        self.participants = participants
        self.start_time = start_time
        self.end_time = end_time
        self.min_occupancy = min_occupancy
        self.max_occupancy = max_occupancy
        self.min_friends = min_friends
        self.max_friends = max_friends
        self.is_accessible = is_accessible
        self._id = _id
        self.company = company
        self.facility = facility

    def save_to_mongodb(self):
        Database.insert(collection='orders', data=self.json())
        # need to be option to save to user

    def json(self):
        return {
            'user_email': self.user_email,
            'date': self.date,
            'participants': self.participants,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'min_occupancy': self.min_occupancy,
            'max_occupancy': self.max_occupancy,
            'min_friends': self.min_friends,
            'max_friends': self.max_friends,
            'is_accessible': self.is_accessible,
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
        orders = []
        for order in data:
            orders.append(cls(**order))
        return orders

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

        # query = {
        #   '$and': [{'date': date}, {'user_email': user_email},
        #           {'$or': [{'$gte': {'start_time': end}}, {'$st': {'end_time': beign}}]}]
        # }
        # query = {
        #   '$and': [{'date': date}, {'user_email': user_email}]

        # }
        data = Database.find('orders', query)
        for order in data:
            orders.append(cls(**order))
        return orders

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
    def already_have_an_order_on_this_time(cls, user_email, date, start_time, end_time):
        orders = cls.find_by_user_email_and_date_and_time(user_email, date, start_time, end_time)
        return True if len(orders) > 0 else False

    @classmethod
    def new_order(cls, user_email, date, participants, start_time, end_time, company, facility, min_permission,
                  min_occupancy, max_occupancy,
                  min_friends, max_friends, is_accessible):
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
        if cls.already_have_an_order_on_this_time(user_email, date, start_time, end_time):
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')

            return False, "user already have an order on that time ", "failed"

        if Schedule.all_participants_are_free(date, participants, start_time, end_time):
            print('ssssssssssssssssssssssssssssss')

            new_order = cls(user_email, date, participants, start_time, end_time, company, facility, min_permission,
                            min_occupancy, max_occupancy,
                            min_friends, max_friends, is_accessible)
            # todo - schedule algorithm, after it run we know the room_id that we will assign them in.
            # todo - this algorithm try to assign the new order into specific room.
            # todo - if it can't do this then it start to chnage other orders.
            status, room_id = new_order.try_schedule_naive_algorithm(company, facility, min_permission,
                                                                     len(participants))

            print(room_id)
            if status:
                new_order.save_to_mongodb()
                return True, new_order._id, room_id
            else:
                all_conflict_orders = Order.find_by_date_and_time(date, start_time, end_time)
                cls.remove_conflict_schedule(all_conflict_orders)
                cls.bactracking_algorithm(all_conflict_orders)

        else:
            print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
            return False, "failed", 'failed'

        return False, " problem with some participants", 'failed'

    @classmethod
    def remove_conflict_schedule(cls, all_conflict_orders):
        for order in all_conflict_orders:
            cls.delete_order(order._id)

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

    def try_schedule_naive_algorithm(self, company, facility, min_permission, participant_num):
        rooms = Room.available_rooms(self.date, participant_num, self.start_time, self.end_time, min_permission,
                                     company, facility, self.min_occupancy, self.max_occupancy,
                                     self.min_friends, self.max_friends, self.is_accessible)

        print('here the rooms available')
        print(rooms)
        for room in rooms:
            if room.avialable_on_time(self.date, self.start_time, self.end_time, participant_num):
                return self._id, room._id
        return False, 'fail'

    @classmethod
    def find_by_facility(cls, company, facility):
        orders = []
        data = Database.find('orders', {'$and': [{'company': company}, {'facility': facility}]})
        if data is not None:
            for order in data:
                orders.append(cls(**order))
        return orders

    @classmethod
    def find_by_date_and_time(cls, date, begin_hour, end_hour):
        orders = []
        query = {
            '$and': [{'date': date}, {'$or': [{'$gt': {'start_time': end_hour}}, {'$st': {'end_time': begin_hour}}]}]
        }
        data = Database.find('orders', query)
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

    @classmethod
    def get_all_participants_in_order(cls, user_email, date, start_time, end_time):
        order = cls.find_by_date_and_time(user_email, date, start_time, end_time)
        if len(order > 0):
            return order.participants
        return []

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


''''
way to do bactracking:

from itertools import permutations

def b3(orders, index_order, rooms, num_rooms):
    if index_order > len(orders)-1:
        return True
    for i in range(num_rooms):
        if orders[index_order]<= rooms[i]:
            rooms[i] = rooms[i] - orders[index_order]
            return b3(orders, index_order+1, rooms, num_rooms)
    return False




orders = [3,2,4,5,6]
rooms = [10,8,6]
perm = permutations(rooms)
for i in list(perm):
    total = b3(orders, 0, list(i), 3)
    if total:
        break
print total
'''
