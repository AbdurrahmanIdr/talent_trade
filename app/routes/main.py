from flask import (
    Blueprint, render_template, url_for,
    redirect, request, flash)
from flask_login import current_user, login_required
from app.utils.email import recieve_email

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def landing():
    return render_template('dashboard/index.html')


@main_bp.route('/contact', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    subject = 'Contact Form Submission'    
    body = f'Name: {name}\nEmail: {email}\nMessage: {message}'

    res, status_code = recieve_email(subject, email, body)
    if status_code == 200:
        flash('Your message has been sent successfully!', 'success')
    else:
        flash(res, 'danger')

    return redirect(url_for('main.landing'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return render_template('admin/dashboard.html')

    elif current_user.role == 'client':
        return redirect(url_for('dashboard.client_dashboard'))

    elif current_user.role == 'freelancer':
        return redirect(url_for('dashboard.freelancer_dashboard'))
    else:
        flash('User-role not found', 'danger')
        return redirect(url_for('main.landing'))
