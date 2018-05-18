from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename

from common.database import Database
import os
import subprocess
from models.User import User, Manager

app = Flask(__name__)
app.secret_key = 'super secret key'
"""Here we write the routes function.
    which it mean that when we try to go to some url (/index)
    the function under that run"""
UPLOAD_FOLDER = 'C:/Users/elyasafb/PycharmProjects/TheDoors/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MAX_PERMISSION = 100


def add_user(req, manager):
    email = req.form['email']
    password = req.form['password']
    username = req.form['username']
    _id = req.form['id']
    permission = req.form['permission']
    facility = req.form['facility']
    role = req.form['role']
    if facility not in manager.get_facilities():
        manager.add_facility(facility)
    if role not in manager.get_roles():
        manager.add_roles(role)
    manager.user_register(email, password, username, _id, role, permission, manager.company, facility)


def remove_user(req, manager):
    email = req.form['email']
    return manager.delete_user(email)


def import_users(request, manager):
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    manager.import_employee(filename)


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
    try:
        if session['email'] is not None:
            user = User.get_by_email(session['email'])
            if user.manager:
                return redirect(url_for('route_analytics'))
            else:
                return redirect(url_for('route_edit_friends'))
    except Exception as e:
        return render_template('page-login.html', wrong_password=False)


@app.route('/login', methods=['POST', 'GET'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)
        if Manager.get_by_email(email) is not None:
            return redirect(url_for('route_analytics'))
        elif User.get_by_email(email) is not None:
            return redirect(url_for('route_edit_friends'))
    else:
        User.logout()
        return render_template('page-login.html', wrong_password=True, email=email)
    return 'hello' + email


@app.route('/register', methods=['GET', 'POST'])
def manager_register():
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
    if session['email'] is not None and Manager.get_by_email(session['email']) is not None:
        return render_template('Simulation.html')


@app.route('/analytics', methods=['GET'])
def route_analytics():
    if session['email'] is not None and Manager.get_by_email(session['email']) is not None:
        return render_template('Analytics.html')


def get_user_roles_facilities(manager):
    roles = manager.get_roles()
    facilities = manager.get_facilities()
    users = manager.get_employees()
    return users, roles, facilities


@app.route('/employee_datatable', methods=['GET', 'POST'])
def route_employee_datatable():
    manager = Manager.get_by_email(session['email'])
    if session['email'] is not None and manager is not None:
        if request.method == 'GET':
            users, roles, facilities = get_user_roles_facilities(manager)
            return render_template('Employee-datatable.html', users=users, roles=roles, facilities=facilities)
        elif request.method == 'POST':
            if request.form['type'] == 'add_user':
                add_user(request, manager)
            elif request.form['type'] == 'remove_user':
                if remove_user(request, manager):
                    flash("Deleted Successfully")
                else:
                    flash("Delete Failed")
            elif request.form['type'] == 'import_users':
                print(request.form)
                print(request.files)
                import_users(request, manager)
            users, roles, facilities = get_user_roles_facilities(manager)
            return render_template('Employee-datatable.html', users=users, roles=roles, facilities=facilities)


@app.route('/rooms_datatable', methods=['GET'])
def route_rooms_datatable():
    if session['email'] is not None and Manager.get_by_email(session['email']) is not None:
        return render_template('Rooms-datatable.html')


@app.route('/edit_friends', methods=['GET'])
def route_edit_friends():
    if session['email'] is not None:
        email = session['email']
        user = User.get_by_email(email)
        friends = user.get_friends()
        return render_template('friends_page.html', manager=user.manager, friends=friends)


@app.route('/reserve_room', methods=['GET'])
def route_reserve_room():
    if session['email'] is not None:
        if request.method == 'GET':
            email = session['email']
            user = User.get_by_email(email)
            return render_template('order.html', manager=user.manager)


@app.route('/my_reservations', methods=['GET'])
def route_reservations():
    if session['email'] is not None:
        email = session['email']
        user = User.get_by_email(email)
        return render_template('reservation.html', manager=user.manager)


@app.before_first_request
def initialize_database():
    # p()
    Database.initialize()


if __name__ == '__main__':
    app.run()
