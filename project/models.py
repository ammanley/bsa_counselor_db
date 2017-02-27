from project import db, bcrypt
from flask_login import UserMixin
from flask import request

join_table = db.Table('counselors_merit_badges',
	db.Column('counselor_id', db.Integer, db.ForeignKey('counselors.id')),
	db.Column('merit_badge_id',db.Integer, db.ForeignKey('merit_badges.id'))
	)
# Why is this table empty even tho refs are working?

class Counselor(db.Model, UserMixin):

	__tablename__ = 'counselors'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.Text)
	password = db.Column(db.Text)
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	email = db.Column(db.Text)
	phone = db.Column(db.BigInteger)
	address = db.Column(db.Text)
	badges = db.relationship('MeritBadge', secondary=join_table,
		backref=db.backref('counselors')
		)

	@classmethod
	def new_for_form(cls, form):
		return Counselor(
			username = request.form['username'],
			password = request.form['password'],
			email = request.form['email']
			)

	def __init__(self, username, password, email, first_name=None, last_name=None, phone=None, address=None):
		self.username = username
		self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.phone = phone 
		self.address = address 

	def __repr__(self):
		return "ID: {}, Username: {}, Email: {} - Badges Counseled: {}".format(self.id, self.username, self.email, self.badges)


class MeritBadge(db.Model, UserMixin):

	__tablename__ = 'merit_badges'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.Text)
	eagle_required = db.Column(db.Boolean)
	# backref to counselor

	@classmethod
	def new_for_form(cls, form):
		return MeritBadge(
			name = request.form['name'],
			eagle_required = form.eagle_required.data
			)

	def __init__(self,name,eagle_required):
		self.name = name 
		self.eagle_required = eagle_required

	def __repr__(self):
		return "Name: {}, Eagle Required?: {}".format(self.name, self.eagle_required)



