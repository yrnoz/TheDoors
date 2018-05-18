import pytest
import os
import subprocess

from datetime import datetime

from common.database import Database
from models.Room import Room
from models.Schedule import Schedule
from models.User import Manager, User
from models.facilities import Facilities
from models.friends import Friends


@pytest.fixture(autouse=True)
def p():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    yield p
    p.terminate()


def test_user():
    Database.initialize()
    Manager.manager_register("admin@yahoo.com", 'admin', 'Admin admin', '000000000', 'eng', 1, 'YAHOO', 'matam')

    Manager.user_register("email@gmail.com", '123', 'ely', '000000026', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("user@yahoo.com", '123', 'yosi', '023412349', 'eng', 1, 'YAHOO', 'matam')
    Manager.user_register("user2@yahoo.com", '123', 'dave', '123412348', 'eng', 1, 'YAHOO', 'matam')
    Manager.user_register("email_1@gmail.com", '123', 'foox', '000002600', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("email_2@gmail.com", '123', 'avi', '000260000', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("email_3@gmail.com", '123', 'yin', '000000026', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("email_4@gmail.com", '123', 'yan', '026000000', 'eng', 3, 'YAHOO', 'matam')

    assert User.get_by_id("email@gmail.com") is None
    assert User.get_by_id("000000000") is not None
    assert User.get_by_email("admin@yahoo.com").company == 'YAHOO'
    assert User.get_by_email('user@yahoo.com').company == 'YAHOO'
    assert User.get_by_email("user2@yahoo.com").company == 'YAHOO'

    assert User.login_valid('email_4@gmail.com', '123') is True
    assert User.login_valid('email_4@gmail.com', 'username__') is False

    manager = Manager.get_by_email('user@yahoo.com')
    assert manager is None
    manager = Manager.get_by_email('admin@yahoo.com')
    assert manager is not None
    assert manager.delete_user('user@yahoo.com') is True
    assert User.get_by_email('user@yahoo.com') is None
    assert manager.delete_user('email_3@gmail.com') is False

    assert manager.delete_user('aaaaaaaaaaaaa') is False
    assert User.min_permission(['email_4@gmail.com', "user2@yahoo.com", "admin@yahoo.com"]) == 1
    assert User.min_permission(['email_4@gmail.com', 'email_1@gmail.com']) == 3
    assert manager.update_user('manager') is True


def test_rooms():
    Database.initialize()
    Database.remove('rooms', {})
    status, room_id = Room.add_room(2, 30, 1, 3, 'YAHOO', 'matam', True)
    assert status is True
    status, room_id = Room.add_room(2, 30, 3, 4, 'YAHOO', 'matam', False)
    assert status is True
    assert Room.remove_room(room_id) is True
    status, room_id = Room.add_room(2, 30, 3, 4, 'YAHOO', 'matam', True)
    assert status is True
    assert Room.get_by_id(room_id).company == 'YAHOO'
    assert len(Room.get_by_company('YAHOO')) > 0
    assert len(Room.get_by_facility('YAHOO', 'matam')) > 0
    assert len(Room.get_by_capacity(5, 'YAHOO', 'matam', 2)) > 0
    assert len(Room.get_by_capacity(50, 'YAHOO', 'matam', 2)) == 0
    assert len(Room.get_by_capacity(20, 'YAHOO', 'matam', 3)) > 0
    assert len(Room.get_by_capacity(20, 'YAHOO', 'matam', 1)) == 0
    assert len(Room.available_rooms('11/11/11', 12, 1, 2, 2, 'YAHOO', 'matam')) > 0


def test_schedules_orders():
    user = User.get_by_email('email_1@gmail.com')
    participants = ['email_1@gmail.com', 'email_2@gmail.com']
    date = datetime.utcnow().strftime('%d/%m/%y')
    status, string = user.new_order(date, participants, 1, 2, "YAHOO", 'matam')
    print(string)
    assert len(user.get_orders()) > 0
    schedules = user.get_schedule()
    assert len(schedules) > 0
    schedules = Schedule.get_schedules('email_1@gmail.com')
    for sched in schedules:
        sched.get_order_id()
        sched.future_meeting()
    assert len(Schedule.get_by_room("YAHOO matam 1")) > 0


def test_facilities():
    Database.initialize()
    # add company

    status = Facilities.is_company_exist('google')
    assert status != Facilities.add_company('google', 'matam')
    status = Facilities.is_company_exist('yahoo')
    assert status != Facilities.add_company('yahoo', 'matam')
    status = Facilities.is_company_exist('microsoft')
    assert status != Facilities.add_company('microsoft', 'matam')
    status = Facilities.is_company_exist('vmware')
    assert status != Facilities.add_company('vmware', 'matam')
    status = Facilities.is_company_exist('intel')
    assert status != Facilities.add_company('intel', 'matam')
    # add facilities to each company

    status = Facilities.is_facility_exist('google', 'carmel')
    assert status != Facilities.add_facility('google', 'carmel')
    status = Facilities.is_facility_exist('yahoo', 'carmel')
    assert status != Facilities.add_facility('yahoo', 'carmel')
    status = Facilities.is_facility_exist('microsoft', 'carmel')
    assert status != Facilities.add_facility('microsoft', 'carmel')
    status = Facilities.is_facility_exist('vmware', 'carmel')
    assert status != Facilities.add_facility('vmware', 'carmel')
    status = Facilities.is_facility_exist('intel', 'carmel')
    assert status != Facilities.add_facility('intel', 'carmel')

    assert 'carmel' in Facilities.get_facilities('intel')
    assert 'matam' in Facilities.get_facilities('intel')
    assert 'carmel' in Facilities.get_facilities('vmware')
    assert 'matam' in Facilities.get_facilities('vmware')

    Facilities.remove_facility('vmware', 'carmel')
    assert 'carmel' not in Facilities.get_facilities('vmware')


def test_friends():
    Database.initialize()

    user1 = User.get_by_email("email_1@gmail.com")
    user2 = User.get_by_email('email_2@gmail.com')
    user3 = User.get_by_email('email_3@gmail.com')
    user4 = User.get_by_email('email_4@gmail.com')

    user1.add_friend('email_2@gmail.com')
    status, string = user1.add_friend('email_3@gmail.com')
    assert status is False
    user1.add_friend('email_4@gmail.com')

    assert user2.email in user1.get_friends_emails()
    assert user3 not in user1.get_friends_emails()
    assert user4.email in user1.get_friends_emails()

    user1.remove_friend('email_4@gmail.com')
    assert 'email_4@gmail.com' not in user1.get_friends_emails()

    assert 'email_1@gmail.com' in user2.get_friends_emails()
    assert not Friends.is_friends('email_1@gmail.com', 'email_4@gmail.com')
    assert Friends.is_friends('email_1@gmail.com', 'email_2@gmail.com')

    manager = Manager.get_by_email('admin@yahoo.com')
    assert len(manager.get_friends()) == 0

    assert len(user1.get_friends()) > 0

    manager.add_friend('email_1@gmail.com')
