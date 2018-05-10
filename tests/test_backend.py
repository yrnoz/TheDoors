import pytest
import os
import subprocess

from common.database import Database
from models.Room import Room
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
    Manager.manager_register("mang@yahoo.com", '123', 'username', '000000000', 'eng', 1, 'YAHOO', 'matam')

    Manager.user_register("email@gmail.com", '123', 'username', '000000026', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("user@yahoo.com", '123', 'username', '023412349', 'eng', 1, 'YAHOO', 'matam')
    Manager.user_register("user2@yahoo.com", '123', 'username', '123412348', 'eng', 1, 'YAHOO', 'matam')
    Manager.user_register("email_1@gmail.com", '123', 'username', '000002600', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("email_2@gmail.com", '123', 'username', '000260000', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("email_3@gmail.com", '123', 'username', '000000026', 'eng', 3, 'YAHOO', 'matam')
    Manager.user_register("email_4@gmail.com", '123', 'username', '026000000', 'eng', 3, 'YAHOO', 'matam')

    assert User.get_by_id("email@gmail.com") is None
    assert User.get_by_id("000000000") is not None
    assert User.get_by_email("mang@yahoo.com").company == 'YAHOO'
    assert User.get_by_email('user@yahoo.com').company == 'YAHOO'
    assert User.get_by_email("user2@yahoo.com").company == 'YAHOO'

    assert User.login_valid('email_4@gmail.com', 'username') is True
    assert User.login_valid('email_4@gmail.com', 'username__') is False

    manager = Manager.get_by_email('user@yahoo.com')
    assert manager is None
    manager = Manager.get_by_email('mang@yahoo.com')
    assert manager is not None
    assert manager.delete_user('user@yahoo.com') is True
    assert User.get_by_email('user@yahoo.com') is None
    assert manager.delete_user('email_3@gmail.com') is False

    assert manager.delete_user('aaaaaaaaaaaaa') is False
    assert User.min_permission(['email_4@gmail.com', "user2@yahoo.com", "mang@yahoo.com"]) == 1
    assert User.min_permission(['email_4@gmail.com', 'email_1@gmail.com']) == 3
    assert manager.update_user('manager') is True


def test_rooms():
    Database.initialize()
    Database.remove('rooms', {})
    status, room_id = Room.add_room(2, 30, 1, 3, 'google', 'matam')
    assert status is True
    status, room_id = Room.add_room(2, 30, 3, 4, 'google', 'matam')
    assert status is True
    assert Room.remove_room(room_id) is True
    status, room_id = Room.add_room(2, 30, 3, 4, 'google', 'matam')
    assert status is True
    assert Room.get_by_id(room_id).company == 'google'
    assert len(Room.get_by_company('google')) > 0
    assert len(Room.get_by_facility('google', 'matam')) > 0
    assert len(Room.get_by_capacity(5, 'google', 'matam', 2)) > 0
    assert len(Room.get_by_capacity(50, 'google', 'matam', 2)) == 0
    assert len(Room.get_by_capacity(20, 'google', 'matam', 3)) > 0
    assert len(Room.get_by_capacity(20, 'google', 'matam', 1)) == 0
    assert len(Room.available_rooms('11/11/11', 12, 1, 2, 2, 'google', 'matam')) > 0


def test_schedules():
    # todo
    pass


def test_orders():
    # todo
    pass


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

    user = User.get_by_email("email_1@gmail.com")

    user.add_friend('email_2@gmail.com')
    status, string = user.add_friend('email_3@gmail.com')
    assert status is False
    user.add_friend('email_4@gmail.com')

    assert 'email_2@gmail.com' in user.get_friends()
    assert 'email_3@gmail.com' not in user.get_friends()
    assert 'email_4@gmail.com' in user.get_friends()

    user.remove_friend('email_4@gmail.com')
    assert 'email_4@gmail.com' not in user.get_friends()

    user = User.get_by_email("email_2@gmail.com")
    assert 'email_1@gmail.com' in user.get_friends()
    assert not Friends.is_friends('email_1@gmail.com', 'email_4@gmail.com')
    assert Friends.is_friends('email_1@gmail.com', 'email_2@gmail.com')
    manager = Manager.get_by_email('mang@yahoo.com')
    assert len(manager.get_friends()) == 0
    user = User.get_by_email('email_1@gmail.com')
    assert len(user.get_friends()) > 0
