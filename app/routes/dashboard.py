from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
# from app.utils.helpers import get_unread_message_count

# Create a Blueprint for the dashboard
dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/client/dashboard')
@login_required
def client_dashboard():
    if current_user.role != 'client':
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('main.landing'))
    
    # Fetch the jobs posted by the current client
    jobs = current_user.posted_jobs
    payments = current_user.payments_made
        
    # unread_message_count = get_unread_message_count(current_user.id)

    return render_template('dashboard/client_dashboard.html', jobs=jobs, payments=payments)


@dashboard_bp.route('/freelancer/dashboard')
@login_required
def freelancer_dashboard():
    if current_user.role != 'freelancer':
        flash('You are not authorized to view this page.', 'danger')
        return redirect(url_for('main.landing'))
    
    # Fetch the jobs assigned to the freelancer
    jobs = current_user.freelancer_jobs
    applications = current_user.applications
    reviews = current_user.reviews_received
    # unread_message_count = get_unread_message_count(current_user.id)

    return render_template('dashboard/freelancer_dashboard.html', jobs=jobs, applications=applications, reviews=reviews)
