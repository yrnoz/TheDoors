from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,IntegerField
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


class EmployeeDelateForm(FlaskForm):#todo
    search = StringField('search id or name', validators=[DataRequired()])
    submit_button_delete = SubmitField('Delete')

class RoomSearchForm(FlaskForm):
    search = StringField('search id', validators=[DataRequired()])
    submit_button_search = SubmitField('Search')


class RoomUpdateForm(FlaskForm):
    room_id = StringField('id', validators=[DataRequired()])
    floor = IntegerField('Floor',validators=[DataRequired()])
    maxCapacity = IntegerField('MaxCapacity', validators=[DataRequired()])
    permission = IntegerField('Permission', validators=[DataRequired()])
    submit_button_update = SubmitField('Update')


class RoomDelateForm(FlaskForm):#todo
    search = StringField('search id', validators=[DataRequired()])
    submit_button_delete = SubmitField('Delete')
