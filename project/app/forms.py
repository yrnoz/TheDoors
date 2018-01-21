from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired

TIME_HOUR = [('1', '8:00'), ('2', '9:00'), ('3','10:00'), ('4', '11:00'), ('4', '11:00'), ('5', '12:00'), ('6', '13:00'),
             ('7', '14:00'), ('8', '15:00'), ('9', '16:00'), ('10', '17:00'), ('11', '18:00'), ('12', '19:00'), ('13', '20:00'),
             ('12', '21:00')]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class EmployeeSearchForm(FlaskForm):
    search = StringField('search room or user id', validators=[DataRequired()])
    submit_employee_search = SubmitField('Search')


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
