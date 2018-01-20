import subprocess
# import client as client
import os
from flask import render_template, flash, redirect, url_for, request, session, send_from_directory
from flask_login import login_user, logout_user, login_required
from werkzeug.datastructures import FileStorage

from config import Config
from app import app, db
from app.Database.ManageDB import *
from app.forms import *
from app.models import User, Room

flag = 0


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        logout_user()
    except:
        pass
    form = LoginForm()
    global flag
    if flag == 0:
        User.drop_collection()
        Room.drop_collection()

        import_employees_from_file('employees_test.csv')
        import_room_details_from_file('rooms_test.csv')

        flag = 1
    if form.validate_on_submit():
        try:
            user = User.objects.get(username=form.username.data)
            if user is not None:
                if user.password == form.password.data:
                    login_user(user)
                    if user.access_permission == 100:
                        return redirect(url_for('managerInterface'))
                    else:
                        return redirect(url_for('userInterface'))
        except:
            pass
    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html', title='Home')


@app.route('/userInterface', methods=['GET', 'POST'])
@login_required
def userInterface():
    return render_template('userInterface.html', title='userInterface')


@app.route('/managerInterface', methods=['GET', 'POST'])
@login_required
def managerInterface():
    return render_template('managerInterface.html', title='userInterface')


# @app.route('/room_recommendation_page', methods=['GET', 'POST'])
# @login_required
# def room_recommendation_page():
#     return render_template('room_recommendation_page.html', title='userInterface')
#

@app.route('/upload_weekly_schedule', methods=['GET', 'POST'])
def upload_weekly_schedule():
    if (session['user_id']):
        flash(session['user_id'])
    else:
        flash('what the fuck')
    # get the 'newfile' field from the form
    new_file = request.files['file']
    # only allow upload of text files
    if new_file.content_type != 'application/vnd.ms-excel':
        flash('only csv files are allowed!')
        return redirect(url_for('weekly_schedule_page'))
    save_path = os.path.join(Config.UPLOAD_DIR, new_file.filename)
    new_file.save(save_path)
    try:
        add_weekly_schedule_for_employee(session['user_id'], Config.UPLOAD_DIR + new_file.filename)
    except:
        flash('import file failed, wrong file')
        return redirect(url_for('weekly_schedule_page'))

    # redirect to home page if it all works ok
    flash('importing schedule succeeded!')
    return redirect(url_for('weekly_schedule_page'))


@app.route('/weekly_schedule_page', methods=['GET', 'POST'])
@login_required
def weekly_schedule_page():
    return render_template('weekly_schedule_page.html', title='userInterface')


@app.route('/editEmployeesByThem', methods=['GET', 'POST'])
@login_required
def editEmployeesByThem():
    return render_template('editEmployeesByThem.html', title='userInterface')


@app.route('/import_rooms', methods=['GET', 'POST'])
@login_required
def import_rooms():
    return render_template('import_rooms.html', title='userInterface')


@app.route('/editDB', methods=['GET', 'POST'])
@login_required
def editDB():
    return render_template('editDB.html', title='userInterface')


@app.route('/import_employees', methods=['GET', 'POST'])
@login_required
def import_employees():
    return render_template('import_employees.html', title='userInterface')


@app.route('/upload_employees', methods=['GET', 'POST'])
def upload_employees():
    """Handle file upload form"""

    # get the 'newfile' field from the form
    newfile = request.files['file']

    # only allow upload of text files
    if newfile.content_type != 'application/vnd.ms-excel':
        flash('only csv files')
        return redirect(url_for('import_employees'))

    save_path = os.path.join(Config.UPLOAD_DIR, newfile.filename)
    newfile.save(save_path)
    try:
        import_employees_from_file(Config.UPLOAD_DIR + newfile.filename)
    except:
        flash('import file failed, wrong file')
        return redirect(url_for('import_employees'))

    # redirect to home page if it all works ok
    flash('import file success')
    return redirect(url_for('import_employees'))


@app.route('/upload_rooms', methods=['GET', 'POST'])
def upload_rooms():
    """Handle file upload form"""

    # get the 'newfile' field from the form
    newfile = request.files['file']

    # only allow upload of text files
    if newfile.content_type != 'application/vnd.ms-excel':
        flash("Only csv files allowed")
        return redirect(url_for('import_rooms'))

    save_path = os.path.join(Config.UPLOAD_DIR, newfile.filename)
    newfile.save(save_path)
    try:
        print str(Config.UPLOAD_DIR)
        print str(newfile.filename)
        import_room_details_from_file(str(Config.UPLOAD_DIR + newfile.filename))

    except Exception as e:
        print e
        flash('import file failed, wrong file')
        return redirect(url_for('import_rooms'))

    # redirect to home page if it all works ok
    flash('import file success')
    return redirect(url_for('import_rooms'))


@app.route('/room_recommendation_page', methods=['GET', 'POST'])
@login_required
def room_recommendation_page():
    form_recommend = roomRecommendationPage()
    if form_recommend.validate_on_submit():
        return form_room_recommend(form_recommend)
    return render_template('room_recommendation_page.html', form_recommend=form_recommend)


def form_room_recommend(form_recommend):
    recommendedList = []
    form_recommend = roomRecommendationPage()
    for room in Rooms.objects.all():
        if room.access_permission > find_employee(session['user_id']).access_permission:
            continue
        schedule_date_time = Schedule()
        for schedule in room.schedules:
            if schedule.date == form_recommend.date and schedule.time == form_recommend.start_time:
                schedule_date_time = schedule
                break
        if 1 <= room.maxCapacity - schedule_date_time.occupancy:
            reccomendedList.append(room.room_id)
    return render_template('room_recommendation_page.html', output=recommendedList, form_recommend=form_recommend)


#########################################edit employees functions######################################################

@app.route('/searchData', methods=['GET', 'POST'])
@login_required
def searchData():
    search = EmployeeSearchForm()
    employee = None
    room = None
    if search.validate_on_submit():
        print("search {}".format(search.search.data))
        try:
            employee = User.objects.get(user_id=search.search.data)
        except:
            try:
                room = Room.objects.get(room_id=search.search.data)
            except:
                flash('user id not exist\n room id not found')
    return render_template('searchDB.html', search=search,
                           employee=employee, room=room)


@app.route('/updateEmployees', methods=['GET', 'POST'])
@login_required
def updateEmployees():
    form_delete = EmployeeDeleteForm()
    form_search = EmployeeSearchForm()
    form_update = EmployeeUpdateForm()
    user = None

    if form_update.validate_on_submit():
        print("in update {} {} {} {}".format(form_update.user_id.data, form_update.permission.data,
                                             form_update.username.data,
                                             form_update.role.data))
        print("update {}".format(form_update.user_id.data))
        try:
            user = User.objects.get(user_id=form_update.user_id.data)
            user.update(username=form_update.username.data, access_permission=form_update.permission.data,
                        role=form_update.role.data)
            user.save()
            user = User.objects.get(user_id=form_update.user_id.data)
        except:
            flash('user id not exist')
            user = None
    else:
        flash("missing data")
    return render_template('editEmployees.html', form_search=form_search, form_delete=form_delete,
                           form_update=form_update, data=user)


@app.route('/deleteData', methods=['GET', 'POST'])
@login_required
def deleteData():
    search = EmployeeDeleteForm()
    if search.validate_on_submit():
        print("delete {}".format(search.search.data))
        try:
            user = User.objects.get(user_id=search.search.data)
            user.delete()
            flash('SUCCESS!\nuser {} deleted'.format(search.search.data))
        except:
            try:
                room = Room.objects.get(room_id=search.search.data)
                room.delete()
                flash('SUCCESS!\nroom {} deleted'.format(search.search.data))
            except:
                flash('no such room or user to delete')

    return render_template('deleteDB.html', search=search)


@app.route('/user_add_friends', methods=['GET', 'POST'])
@login_required
def user_add_friends():
    return render_template('user_add_friends.html', title='editEmployeesByThem')


@app.route('/changePassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    return render_template('changePassword.html', title='editEmployeesByThem')


#########################################edit rooms functions######################################################


@app.route('/editRooms', methods=['GET', 'POST'])
@login_required
def editRooms():
    form_update = RoomUpdateForm()

    room = None
    if form_update.validate_on_submit():
        try:
            room = Room.objects.get(room_id=form_update.room_id.data)
            room.update(floor=form_update.floor.data, access_permission=form_update.permission.data,
                        maxCapacity=form_update.maxCapacity.data)
            room.save()
            room = Room.objects.get(room_id=form_update.room_id.data)
            flash("update Success")
        except:
            flash("update Fail\n maybe missing data")

    return render_template('editRooms.html',
                           form_update=form_update, data=room)

    print(str(select.rooms.choices))
    return render_template('editRooms.html', select=select,
                           form_update=form_update)


@app.route('/editEmployees', methods=['GET', 'POST'])
@login_required
def editEmployees():
    form_update = EmployeeUpdateForm()

    user = None
    if form_update.validate_on_submit():
        try:
            user = User.objects.get(user_id=form_update.user_id.data)
            user.update(username=form_update.username.data, access_permission=form_update.permission.data,
                        role=form_update.role.data)
            user.save()
            user = User.objects.get(user_id=form_update.user_id.data)
            flash("update Success")
        except:
            flash("update Fail\n maybe missing data")

    return render_template('editEmployees.html',
                           form_update=form_update, data=user)

    print(str(select.rooms.choices))
    return render_template('editEmployees.html', select=select,
                           form_update=form_update)


##############################################exportTables######################################################3
@app.route('/exportTables', methods=['GET', 'POST'])
@login_required
def exportTables():
    try:
        os.remove('employees_DB.csv')
        os.remove('rooms_DB.csv')
    except:
        pass
    employee_form = exportEmployeeForm()
    room_form = exportRoomForm()
    return render_template('exportTables.html', room_form=room_form, employee_form=employee_form)


@app.route('/exportRooms', methods=['GET', 'POST'])
@login_required
def exportRooms():
    dir_path = Config.DOWNLOAD_DIR
    rooms_file = 'rooms_DB.csv'
    try:
        os.remove('employees_DB.csv')
        os.remove('rooms_DB.csv')
    except:
        pass
    export_rooms_to_file(rooms_file)
    return send_from_directory(directory=dir_path, filename='rooms_DB.csv')


@app.route('/exportEmployees', methods=['GET', 'POST'])
@login_required
def exportEmployees():
    dir_path = Config.DOWNLOAD_DIR
    employees_file = 'employees_DB.csv'
    try:
        os.remove('employees_DB.csv')
        os.remove('rooms_DB.csv')
    except:
        pass
    export_employees_to_file(employees_file)
    return send_from_directory(directory=dir_path, filename='employees_DB.csv')


@app.route('/searchDB', methods=['GET', 'POST'])
@login_required
def searchDB():
    search = EmployeeSearchForm()
    return render_template('searchDB.html', title='userInterface', search=search)


@app.route('/deleteDB', methods=['GET', 'POST'])
@login_required
def deleteDB():
    search = EmployeeDeleteForm()
    return render_template('deleteDB.html', title='userInterface', search=search)
