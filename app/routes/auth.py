from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request)
from flask_login import login_user, login_required, logout_user, current_user

from app.models.user import User

from app.services import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        response, status = AuthService.login_user(email, password)
        match status:
            case 200:
                user_id = response.get('user_id')
                user = User.query.get(int(user_id))
                login_user(user)
                flash(
                    response.get('message', 'Login successful!'),
                    'success')
                return redirect(url_for('main.dashboard'))
            case 400:
                flash(response.get('error'), 'danger')
            case _:
                flash('Login failed. Check your email and password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role')
        fullname = request.form.get('fullname')

        response, status = AuthService.register_user(username, email, password, role, fullname)
        match status:
            case 201:
                flash(
                    message=response.get(
                        'message',
                        'Registration successful! Please log in.'),
                    category='success'
                )
                return redirect(url_for('auth.login'))
            case 400:
                flash(
                    message=response.get('error', 'mail conflict.'),
                    category='danger'
                )
            case _:
                flash(
                    message=response.get(
                        'message', 
                        'Error with user registration.'),
                    category='danger'
                )

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()    
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
