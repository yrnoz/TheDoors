from flask import Flask, render_template, request, session

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

    return render_template('page-login.html')


@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        return render_template('login.html')
    return render_template('not sure yet.html')


@app.before_first_request
def initialize_database():
    # p()
    Database.initialize()


if __name__ == '__main__':
    app.run()
