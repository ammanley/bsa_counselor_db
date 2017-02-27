from flask import Flask, url_for, redirect
from flask_migrate import Migrate 
from flask_login import current_user, LoginManager
from flask_sqlalchemy import SQLAlchemy 
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CsrfProtect
# for migrations to work


app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/merit_badge_counselors'
app.config['SECRET_KEY'] = 'shhhhhh'
# set this to enviro later
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['TEMPLATES_AUTO_RELOAD'] = True
modus = Modus(app)
db = SQLAlchemy(app)
CsrfProtect(app)

login_manager.login_view = "counselors.login"

from project.models import Counselor, MeritBadge
# must be after db is defined to prevent circular import
from project.counselors.views import counselors_blueprint
from project.merit_badges.views import merit_badges_blueprint


@login_manager.user_loader
def load_user(id):
	return Counselor.query.get(id)

@app.route('/')
def root():
	return "Hi there! Welcome to Root!"


app.register_blueprint(counselors_blueprint, url_prefix = '/counselors')
app.register_blueprint(merit_badges_blueprint, url_prefix='/badges')


# from IPython import embed; embed()