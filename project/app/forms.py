from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired

TIME_HOUR = [('8:00', '8:00'), ('9:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'),
             ('13:00', '13:00'),
             ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'),
             ('19:00', '19:00'), ('20:00', '20:00'),
             ('21:00', '21:00')]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class EmployeeSearchForm(FlaskForm):
    search = StringField('search room or user id', validators=[DataRequired()])
    submit_employee_search = SubmitField('Search')


class EmployeeAddForm(FlaskForm):
    user_id = StringField('id', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    permission = IntegerField('Permission', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit_button_add = SubmitField('Add')


class EmployeeUpdateForm(FlaskForm):
    user_id = StringField('id', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    permission = IntegerField('Permission', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    submit_button_update = SubmitField('Update')


class EmployeeDeleteForm(FlaskForm):
    search = StringField('search room or user id')
    submit_button_delete = SubmitField('Delete')


class RoomSearchForm(FlaskForm):
    search = StringField('search id', validators=[DataRequired()])
    submit_room_search = SubmitField('Search')


class RoomUpdateForm(FlaskForm):
    room_id = StringField('id', validators=[DataRequired()])
    floor = IntegerField('Floor', validators=[DataRequired()])
    maxCapacity = IntegerField('MaxCapacity', validators=[DataRequired()])
    permission = IntegerField('Permission', validators=[DataRequired()])
    submit_button_update = SubmitField('Update')


class RoomAddForm(FlaskForm):
    room_id = StringField('id', validators=[DataRequired()])
    floor = IntegerField('Floor', validators=[DataRequired()])
    maxCapacity = IntegerField('MaxCapacity', validators=[DataRequired()])
    permission = IntegerField('Permission', validators=[DataRequired()])
    submit_button_add = SubmitField('Add')

class RoomDeleteForm(FlaskForm):
    room_id = StringField('id')
    submit_button_delete = SubmitField('Delete')


class roomRecommendationPage(FlaskForm):
    start_time = SelectField('start time', choices=TIME_HOUR, validators=[DataRequired()])
    end_time = SelectField('end time', choices=TIME_HOUR, validators=[DataRequired()])
    submit = SubmitField('recommend')


class exportRoomForm(FlaskForm):  # tod
    submit_room = SubmitField('Rooms csv')


class exportEmployeeForm(FlaskForm):  # tod
    submit_employee = SubmitField('Employee csv')


class selectRoom(FlaskForm):
    rooms = SelectField(
        'Room id',
        choices=[]
    )
    submit = SubmitField('Submit')


class selectEmplyee(FlaskForm):
    ids = SelectField(
        'User id',
        choices=[]
    )
    submit = SubmitField('Submit')


class changePass(FlaskForm):
    old_pass = PasswordField('Previous password', validators=[DataRequired()])
    password = PasswordField('New Password:', validators=[DataRequired()])
    again = PasswordField(' New password again:', validators=[DataRequired()])
    submit = SubmitField('Edit')
