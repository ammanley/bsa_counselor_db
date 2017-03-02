from flask import redirect, render_template, url_for, request, flash, Blueprint
from project.models import Counselor, MeritBadge
from project.counselors.forms import CounselorForm, CounselorEditForm, LoginForm
from project import db, bcrypt
from project import login_manager
from flask_login import current_user, login_required, login_user, logout_user

counselors_blueprint = Blueprint(
	'counselors',
	__name__,
	template_folder = 'templates'
	)

@counselors_blueprint.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST':
		counselor = Counselor.query.filter_by(username=form.username.data).first()
		if counselor:
			if form.validate():
				if bcrypt.check_password_hash(counselor.password, form.password.data):
					flash('You have been logged in.')
					login_user(counselor)
					return redirect(url_for('counselors.index',counselor=counselor))
		flash('Invalid credentials')
		return redirect(url_for('counselors.login', form=form))
	return render_template('counselors/login.html', form=form)

@counselors_blueprint.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out")
	return redirect(url_for('counselors.login'))
	# WHAT IS CACHING WHEN I HIT THE BACK BUTTON?
	# response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')

@counselors_blueprint.route('/')
@login_required
def show_all():
	counselors = Counselor.query.all()
	return render_template('counselors/show_all.html', counselors=counselors)

# check hashes

@counselors_blueprint.route('/home', methods = ['GET','POST'])
@login_required
def index():
	counselor = current_user
	# from IPython import embed; embed()
	# counselor = Counselor.query.filter_by(username=form.username.data).first()
	# return redirect(url_for('counselors.login', form=form))
	return render_template('counselors/index.html', counselor=counselor)
	return redirect
	# find and add cache time limit


@counselors_blueprint.route('/<int:id>', methods=['GET','PATCH','DELETE'])
@login_required
def show(id):
	counselor = Counselor.query.get(id)
	form = CounselorEditForm(request.form)
	if request.method == b'PATCH':
		if form.validate_on_submit():
			# why does form.validate break this with "NoneType" Object is not iterable?
			counselor.username = form.username.data
			counselor.password= bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
			counselor.first_name=form.first_name.data
			counselor.last_name=form.last_name.data
			counselor.email=form.email.data
			counselor.phone=form.phone.data
			counselor.address=form.address.data
			counselor.badges = counselor.badges.append(form.badges.data)
			# this seems to break validation
			db.session.add(counselor)
			db.session.commit()
			flash('Changes submitted.')
			return redirect(url_for('counselors.show',id=id))
		flash('Please make corrections before submitting.')
		# Why do error messages not propgage?
		return redirect(url_for('counselors.edit', id=id, form=form))
	if request.method == b'DELETE':
		db.session.delete(counselor)
		db.session.commit()
		flash('Account deleted. Sorry to see you go.')
		return redirect(url_for('counselors.index'))
	return render_template('/counselors/show.html', counselor=counselor)


@counselors_blueprint.route('/<int:id>/edit')
@login_required
def edit(id):
	counselor = Counselor.query.get(id)
	form = CounselorEditForm(obj=counselor)
	form.badges.choices = [(badge.id, badge.name) for badge in MeritBadge.query.all()]
	return render_template('/counselors/edit.html', counselor=counselor, form=form, id=id)


@counselors_blueprint.route('/signup', methods=['GET','POST'])
def new():
	form = CounselorForm(request.form)
	if request.method == 'POST':

		if form.validate():
			new_counselor = Counselor.new_for_form(form)
			db.session.add(new_counselor)
			db.session.commit()
			flash("Thank you for singing up. You can now add your address and other personal info through the edit page after you log in.")
			return redirect(url_for('counselors.login'))
		flash('Please fill in all fields.')
	return render_template('counselors/new.html', form=form)