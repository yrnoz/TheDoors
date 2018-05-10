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
    # todo
    Manager.user_register("email@gmail.com", '123', 'username', '000000026', 'eng', 3, 'google', 'matam')
    Manager.manager_register("mang@yahoo.com", '123', 'username', '000000000', 'eng', 1, 'YAHOO', 'matam')
    Manager.user_register("user@yahoo.com", '123', 'username', '023412349', 'eng', 1, 'YAHOO', 'matam')
    Manager.user_register("user2@yahoo.com", '123', 'username', '123412348', 'eng', 1, 'YAHOO', 'matam')

    assert User.get_by_email("email@gmail.com") is None
    assert User.get_by_email("mang@yahoo.com").company == 'YAHOO'
    assert User.get_by_email('user@yahoo.com').company == 'YAHOO'
    assert User.get_by_email("user2@yahoo.com").company == 'YAHOO'

    manager = Manager.get_by_email('user@yahoo.com')
    assert manager is None
    manager = Manager.get_by_email('mang@yahoo.com')
    assert manager is not None
    assert manager.delete_user('user@yahoo.com') is True
    assert User.get_by_email('user@yahoo.com') is None
    assert manager.delete_user('email_3@gmail.com') is False

    # user.new_order('15/12/18', ['user2@yahoo.com', 'mang@yahoo.com'], 1, 2)
    # order_id = 'user@yahoo.com15/12/1812'
    # user.cancel_order(order_id)


def test_rooms():
    Database.initialize()
    # todo
    status, room_id = Room.add_room(2, 30, 1, 3, 'google', 'matam')
    status, room_id = Room.add_room(2, 30, 3, 4, 'google', 'matam')


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
    Manager.user_register("email_1@gmail.com", '123', 'username', '000002600', 'eng', 3, 'google', 'matam')
    Manager.user_register("email_2@gmail.com", '123', 'username', '000260000', 'eng', 3, 'google', 'matam')
    Manager.user_register("email_3@gmail.com", '123', 'username', '000000026', 'eng', 3, 'google', 'matam')
    Manager.user_register("email_4@gmail.com", '123', 'username', '026000000', 'eng', 3, 'google', 'matam')

    user = User.get_by_email("email_1@gmail.com")

    user.add_friend('email_2@gmail.com')
    user.add_friend('email_3@gmail.com')
    user.add_friend('email_4@gmail.com')

    assert 'email_2@gmail.com' in user.get_friends()
    assert 'email_3@gmail.com' in user.get_friends()
    assert 'email_4@gmail.com' in user.get_friends()

    user.remove_friend('email_4@gmail.com')
    assert 'email_4@gmail.com' not in user.get_friends()

    user = User.get_by_email("email_2@gmail.com")
    assert 'email_1@gmail.com' in user.get_friends()
    assert not Friends.is_friends('email_1@gmail.com', 'email_4@gmail.com')
    assert Friends.is_friends('email_1@gmail.com', 'email_3@gmail.com')
