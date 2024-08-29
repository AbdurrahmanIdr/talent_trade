import os

from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, request, current_app, session)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename


from app import db
from app.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile/', methods=['GET'])
@login_required
def profile():
    try:
        return render_template('user/profile.html', user=current_user)
    
    except Exception:
        flash('Error while navigating to user profile', 'danger')
        return redirect(url_for('main.dashboard'))

@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = current_user.id
    user = current_user

    if user is None:
        flash('User does not exist', 'error')
        return redirect(url_for('user.profile', user_id=user_id))

    if request.method == 'GET':
        return render_template('user/edit_profile.html', user=user)

    if request.method == 'POST':
        # Update basic info
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.full_name = request.form.get('full_name')
        user.bio = request.form.get('bio')

        # Handle profile picture upload
        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture and profile_picture.filename:
                filename_ext = str(profile_picture.filename).split('.')[-1]
                filename_comp = f'{user.username}.{filename_ext}'
                filename = secure_filename(filename_comp)
                profile_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                profile_picture.save(profile_picture_path)
                user.profile_picture = filename

        # Update password if provided
        password = request.form.get('password')
        if password:
            user.set_password(password)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile', user_id=user.id))
