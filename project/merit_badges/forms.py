from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, validators

class NewBadge(FlaskForm):
	name = StringField('Badge Name', [validators.InputRequired()])
	eagle_required = BooleanField('Eagle Required?')