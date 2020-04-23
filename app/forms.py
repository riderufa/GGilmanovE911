from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    date_begin = DateField('date_begin', format='%Y-%m-%d', validators=[DataRequired()])
    date_end = DateField('date_end', format='%Y-%m-%d', validators=[DataRequired()])
    theme = StringField('theme')
    description = StringField('description')

class LoginForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('password')

class CreateUserForm(FlaskForm):
    email = EmailField('email')
    name = StringField('name')
    password = PasswordField('password')
    password2 = PasswordField('password2')
