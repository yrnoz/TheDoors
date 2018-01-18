from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class EmployeeSearchForm(FlaskForm):
    search = StringField('search id or name', validators=[DataRequired()])
    submit_button_search = SubmitField('Search')


class EmployeeUpdateForm(FlaskForm):
    user_id = StringField('id', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    permission = IntegerField('Permission', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    submit_button_update = SubmitField('Update')


class EmployeeDeleteForm(FlaskForm):
    user_id = StringField('id')
    submit_button_delete = SubmitField('Delete')


class RoomSearchForm(FlaskForm):
    search = StringField('search id', validators=[DataRequired()])
    submit_button_search = SubmitField('Search')


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
    date = DateTimeField('Date', validators=[DataRequired()])
    start_time = SelectField('start time', validators=[DataRequired()])
    end_time = SelectField('end time', validators=[DataRequired()])
    submit_button = SubmitField('recommend')
    # output = OutputField('recommend', validators=[DataRequired()])
    output = SelectField('recommend', validators=[DataRequired()])
