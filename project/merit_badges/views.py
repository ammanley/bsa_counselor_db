from flask import redirect, render_template, url_for, request, flash, Blueprint
from project.models import MeritBadge, Counselor
from project.counselors.forms import CounselorForm, CounselorEditForm
from project.merit_badges.forms import NewBadge
from project import db, bcrypt
from project import login_manager
from flask_login import current_user, login_required, login_user, logout_user


merit_badges_blueprint = Blueprint(
	'merit_badges',
	__name__,
	template_folder = 'templates'
	)


@merit_badges_blueprint.route('/', methods=['GET','POST'])
def index():

	badges = MeritBadge.query.all()
	if request.method == 'POST':
		form = NewBadge(request.form)
		new_badge = MeritBadge.new_for_form(form)
		# had to set this in Model to eagle_required.data to avoid key error
		db.session.add(new_badge)
		db.session.commit()
		flash('Merit Badge Added.')
	return render_template('merit_badges/index.html', badges=badges)


@merit_badges_blueprint.route('/new')
@login_required
def new():
	form = NewBadge(request.form)
	return render_template('/merit_badges/new.html', form=form)