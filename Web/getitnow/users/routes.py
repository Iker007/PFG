from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from getitnow import db, bcrypt
from getitnow.models import User, SelectedProduct
from getitnow.users.utils import store_profile_image, pass_reset_email
from getitnow.users.forms import RegistrationForm, LoginForm, UpdateProfileForm, ResetPassRequestForm, ResetPassForm

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, address=form.address.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'User {form.username.data} successfully registered! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            wanted_page = request.args.get('next')
            if wanted_page:
                return redirect(wanted_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Error loging in. Check provided data and try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    image_file = url_for('static', filename='profile_images/' + current_user.profile_picture)
    selected_products = SelectedProduct.query.all()
    update_form = UpdateProfileForm()
    if update_form.validate_on_submit():
        if update_form.profile_picture.data:
            image_file = store_profile_image(update_form.profile_picture.data)
            current_user.profile_picture = image_file
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        current_user.address = update_form.address.data
        db.session.commit()
        flash('Information succesfully updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
        update_form.address.data = current_user.address
    return render_template('profile.html', title='Profile', profile_picture=image_file, form=update_form, selected_products=selected_products)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/password_reset", methods=['GET', 'POST'])
def request_pass_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    request_reset_form = ResetPassRequestForm()
    if request_reset_form.validate_on_submit():
        user = User.query.filter_by(email=request_reset_form.email.data).first()
        pass_reset_email(user)
        flash('Check your email to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_pass_reset.html', title='Reset password', form=request_reset_form)

@users.route("/password_reset/<token>", methods=['GET', 'POST'])
def pass_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid ', 'warning')
        return redirect(url_for('users.request_pass_reset'))
    reset_form = ResetPassForm()
    if reset_form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(reset_form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Password succesfully changed! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('pass_reset.html', title='Reset password', form=reset_form)