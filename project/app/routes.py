import subprocess
# import client as client
import os

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, session, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user

from config import Config
from app import app, db
from app.Database.ManageDB import *
from app.forms import *
from app.models import User, Room, Schedule

flag = 0

Dict_hours = {'8:00': 1, '9:00': 2, '10:00': 3, '11:00': 4, '12:00': 5,
              '13:00': 6, '14:00': 7, '15:00': 8, '16:00': 9, '17:00': 10, '18:00': 11,
              '19:00': 12, '20:00': 13,
              '21:00': 14}


@app.route('/logout')
def logout():
    logout_user()
    export_rooms_to_file('rooms.csv')
    export_employees_to_file('employees.csv')
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

        import_employees_from_file('employees.csv')
        import_room_details_from_file('rooms.csv')

        flag = 1
    if form.validate_on_submit():
        try:
            user = User.objects.get(username=form.username.data)
            if user is not None:
                if user.password == form.password.data:
                    login_user(user)
                    if user.access_permission == 0:
                        return redirect(url_for('managerInterface'))
                    else:
                        return redirect(url_for('userInterface'))
        except:
            pass
    return render_template('login.html', title='Sign In', form=form)


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))


@app.route('/userInterface', methods=['GET', 'POST'])
@login_required
def userInterface():
    return render_template('userInterface.html', title='userInterface')


@app.route('/managerInterface', methods=['GET', 'POST'])
@login_required
def managerInterface():
    return render_template('managerInterface.html', title='userInterface')


@app.route('/upload_weekly_schedule', methods=['GET', 'POST'])
def upload_weekly_schedule():
    if (session['user_id']):
        flash(session['user_id'])
    else:
        flash('id was not found')
    # get the 'newfile' field from the form
    new_file = request.files['file']
    # only allow upload of text files
    if new_file.content_type != 'application/vnd.ms-excel':
        flash('only csv files are allowed!')
        return redirect(url_for('weekly_schedule_page'))
    save_path = os.path.join(Config.UPLOAD_DIR, new_file.filename)
    new_file.save(save_path)
    try:
        add_weekly_schedule(session['user_id'], Config.UPLOAD_DIR + new_file.filename)
    except:
        flash('import file failed, wrong file')
        return redirect(url_for('weekly_schedule_page'))

    # redirect to home page if it all works ok
    flash('importing schedule succeeded!')
    return redirect(url_for('weekly_schedule_page'))


@app.route('/weekly_schedule_page', methods=['GET', 'POST'])
@login_required
def weekly_schedule_page():
    return render_template('weekly_schedule_page.html', title='userInterface',
                           output=User.objects.get(user_id=session['user_id']).schedules)


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
        import_room_details_from_file(str(Config.UPLOAD_DIR + newfile.filename))

    except Exception as e:
        print e
        flash('import file failed, wrong file')
        return redirect(url_for('import_rooms'))

    # redirect to home page if it all works ok
    flash('import file success')
    return redirect(url_for('import_rooms'))


def cmp_room(room1, room2):
    return room2[1] - room1[1]


def add_sched(rooms, date_time):
    for room in rooms:
        if room.room_id == 'taub 1':
            room.schedules.append(
                Schedule(date=date_time.replace(hour=10).strftime("%d/%m/%y %H"), occupancy=room.maxCapacity))
        if room.room_id == 'taub 2':
            room.schedules.append(
                Schedule(date=date_time.replace(hour=11).strftime("%d/%m/%y %H"), occupancy=room.maxCapacity))
        if room.room_id == 'taub 3':
            room.schedules.append(
                Schedule(date=date_time.replace(hour=12).strftime("%d/%m/%y %H"), occupancy=room.maxCapacity))
            # for room in rooms:
            #     room.schedules.append(Schedule())


def form_room_recommend(form_recommend):
    recommendedList = []
    start_time = Dict_hours[form_recommend.start_time.data]
    end_time = Dict_hours[form_recommend.end_time.data]
    for_hours = end_time - start_time
    date_time = datetime.now()
    list_time = []
    for hour in range(start_time, end_time):
        list_time.append(date_time.replace(hour=hour + 7).strftime("%d/%m/%y %H"))
    rooms = [room for room in Room.objects() if room.access_permission <= current_user.access_permission]
    add_sched(rooms, date_time)

    for room in rooms:
        if not room.schedules:
            recommendedList.append(((room.room_id, room.floor), room.maxCapacity))
        else:
            for schedule in room.schedules:
                count = 0
                factor = 0
                for date in list_time:
                    if schedule.date != date or (1 <= (room.maxCapacity) - int(
                            schedule.occupancy) and schedule.date == date):
                        count += 1
                        factor += room.maxCapacity - schedule.occupancy

                if count == for_hours:
                    recommendedList.append(((room.room_id, room.floor), factor))
    recommendedList = sorted(recommendedList, cmp=cmp_room)
    recommendedList = recommendedList[:7]
    return render_template('room_recommendation_page.html',
                           output=recommendedList, form_recommend=form_recommend)


#########################################edit employees functions######################################################

@app.route('/searchData', methods=['GET', 'POST'])
@login_required
def searchData():
    search = EmployeeSearchForm()
    employee = None
    room = None
    if search.validate_on_submit():
        try:
            employee = User.objects.get(user_id=search.search.data)
        except:
            try:
                room = Room.objects.get(room_id=search.search.data)
            except:
                flash('user id not exist\n room id not found')
    return render_template('searchDB.html', search=search,
                           employee=employee, room=room)


@app.route('/addEmployee', methods=['GET', 'POST'])
@login_required
def addEmployee():
    form_add = EmployeeAddForm()

    user = None
    if form_add.validate_on_submit():
        try:
            user = User(user_id=form_add.user_id.data,
                        username=form_add.username.data,
                        password=form_add.password.data,
                        role=form_add.role.data,
                        access_permission=form_add.permission.data, )
            user.save()
            user = User.objects.get(user_id=form_add.user_id.data)
            flash("Adding Success")
        except:
            flash("Adding Fail\n maybe missing data")

    return render_template('addEmployee.html',
                           form_add=form_add, data=user)


@app.route('/updateEmployees', methods=['GET', 'POST'])
@login_required
def updateEmployees():
    form_delete = EmployeeDeleteForm()
    form_search = EmployeeSearchForm()
    form_update = EmployeeUpdateForm()
    user = None

    if form_update.validate_on_submit():

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
    pass_form = changePass()
    if pass_form.validate_on_submit():
        user = User.objects.get(user_id=current_user.user_id)

        if user.password != pass_form.old_pass.data:
            flash('Wrong password')
        elif pass_form.password.data == pass_form.again.data:
            user.password = pass_form.password.data
            user.save()
            flash('Success')
        else:
            flash('Wrong again password')
    return render_template('changePassword.html', title='editEmployeesByThem', pass_form=pass_form)


#########################################edit rooms functions######################################################


@app.route('/addRoom', methods=['GET', 'POST'])
@login_required
def addRoom():
    form_add = RoomAddForm()

    room = None
    if form_add.validate_on_submit():
        try:
            room = Room(room_id=form_add.room_id.data,
                        floor=form_add.floor.data,
                        maxCapacity=form_add.maxCapacity.data,
                        access_permission=form_add.permission.data)
            room.save()
            room = Room.objects.get(room_id=form_add.room_id.data)
            flash("Adding Success")
        except:
            flash("Adding Fail\n maybe missing data")

    return render_template('addRoom.html',
                           form_add=form_add, data=room)

    return render_template('addRoom.html', select=select,
                           form_add=form_add)


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


@app.route('/show_all_db_rooms', methods=['GET', 'POST'])
@login_required
def show_all_db_rooms():
    search = show_rooms_page()
    return render_template('show_all_db_rooms.html', search=search)


@app.route('/show_all_db_employee', methods=['GET', 'POST'])
@login_required
def show_all_db_employee():
    search = show_employee_page()
    return render_template('show_all_db_employee.html', search=search)


@app.route('/show_all_db', methods=['GET', 'POST'])
@login_required
def show_all_db():
    return render_template('show_all_db.html', title='editDB')


@app.route('/room_recommendation_page', methods=['GET', 'POST'])
@login_required
def room_recommendation_page():
    form_recommend = roomRecommendationPage()
    if form_recommend.validate_on_submit():
        return form_room_recommend(form_recommend)
    return render_template('room_recommendation_page.html', form_recommend=form_recommend)


@app.route('/room_reccomendation', methods=['GET', 'POST'])
@login_required
def room_reccomendation():
    form_recommend = roomRecommendationPage()
    if form_recommend.validate():
        if Dict_hours[form_recommend.start_time.data] >= Dict_hours[form_recommend.end_time.data]:
            flash('start and end time are invalid')
            return render_template('room_recommendation_page.html', form_recommend=form_recommend)
        return form_room_recommend(form_recommend)
    return render_template('room_recommendation_page.html', form_recommend=form_recommend)
