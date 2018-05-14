from flask import Flask, render_template, request, session, redirect

from common.database import Database
import os
import subprocess
from models.User import User, Manager

app = Flask(__name__)
app.secret_key = 'super secret key'
"""Here we write the routes function.
    which it mean that when we try to go to some url (/index)
    the function under that run"""


def p():
    p = subprocess.Popen('mongod', stdout=open(os.devnull, "w"))
    yield p
    p.terminate()


@app.route('/')
def home():
    # Todo
    return render_template('friends_new.html')

    return render_template('page-login.html', wrong_password=False)


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        return render_template('page-login.html', wrong_password=True, email=email)
    return 'hello' + email


@app.route('/register', methods=['GET'])
def manager_register():
    return render_template('page-register.html')


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


@app.before_first_request
def initialize_database():
    # p()
    Database.initialize()


if __name__ == '__main__':
    app.run()
