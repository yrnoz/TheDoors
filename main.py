from flask import Flask, render_template, request, session, redirect, url_for

from common.database import Database
import os
import subprocess
from models.User import User, Manager

app = Flask(__name__)
app.secret_key = 'super secret key'
"""Here we write the routes function.
    which it mean that when we try to go to some url (/index)
    the function under that run"""

MAX_PERMISSION = 100


def p():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    yield p
    p.terminate()


@app.route('/logout')
def logout():
    User.logout()
    return redirect(url_for('home'))


@app.route('/')
def home():
    # Todo
    # return render_template('friends_page.html')

    return render_template('page-login.html', wrong_password=False)


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
        user = Manager.get_by_email(email)
        if user.manager == True:
            return redirect(url_for('route_analytics'))
        else:
            return redirect(url_for('route_friends_new_user'))
    else:
        User.logout()
        return render_template('page-login.html', wrong_password=True, email=email)
    return 'hello' + email


@app.route('/register', methods=['GET', 'POST'])
def manager_register():
    print(request.method)
    if request.method == 'GET':
        return render_template('page-register.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        company = request.form['company']
        facility = request.form['facility']
        username = request.form['username']
        status, info = Manager.manager_register(email, password, username, email, 'Manager', MAX_PERMISSION, company,
                                                facility)
        if status:
            User.login(email)
            return redirect(url_for('route_analytics'))
        else:
            print(info)
            return redirect(url_for('manager_register'))


@app.route('/simulation', methods=['GET'])
def route_simulation():
    return render_template('Simulation.html')


@app.route('/analytics', methods=['GET'])
def route_analytics():
    return render_template('Analytics.html')


@app.route('/employee_datatable', methods=['GET'])
def route_employee_datatable():
    return render_template('Employee-datatable.html')


@app.route('/rooms_datatable', methods=['GET'])
def route_rooms_datatable():
    return render_template('Rooms-datatable.html')


@app.route('/edit_friends', methods=['GET'])
def route_edit_friends():
    return render_template('friends_page.html')


@app.route('/reserve_room', methods=['GET'])
def route_reserve_room():
    return render_template('order.html')


@app.route('/my_reservations', methods=['GET'])
def route_reservations():
    return render_template('reservation.html')




@app.before_first_request
def initialize_database():
    # p()
    Database.initialize()


if __name__ == '__main__':
    app.run()
