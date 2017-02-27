from flask_wtf import FlaskForm
from wtforms import (StringField,PasswordField,IntegerField, SelectField,
SelectMultipleField,validators)

class CounselorForm(FlaskForm):

	username = StringField('Username', [validators.Length(min=3)])
	password = PasswordField('Password', [validators.InputRequired()])
	email = StringField('Email', [validators.Email()])

class CounselorEditForm(FlaskForm):
	username = StringField('Username', [validators.Length(min=3)])
	password = PasswordField('Password', [validators.InputRequired()])
	first_name = StringField('First Name', [validators.Length(max=15)])
	last_name = StringField('Last Name', [validators.Length(max=15)])
	email = StringField('Email', [validators.Email()])
	phone = IntegerField('Phone Number')
	address = StringField('Address', [validators.Length(max=35)])
	badges = SelectMultipleField('Select Badges', coerce=int)

class LoginForm(FlaskForm):

	username = StringField('Username', [validators.Length(min=3)])
	password = PasswordField('Password', [validators.InputRequired()])