from flask import (
    Blueprint, render_template, redirect,
    url_for, flash, jsonify, session,
    request)

from flask_login import current_user, login_required

from app.models import Application, Job
from app.utils.email import recieve_email as send_email
from app.extensions import db
from app.services import application_service


application_bp = Blueprint('application', __name__)


@application_bp.route('/review_application/<int:application_id>', methods=['POST'])
@login_required
def review_application(application_id):
    application = Application.query.get_or_404(application_id)

    if application.is_qualified():
        application.status = 'shortlisted'
        application.user.is_shortlisted = True
        db.session.commit()

        subject = "Congratulations! You’ve Been Shortlisted for TalentTrade"
        recipients = [application.user.email]
        text_body = f"""
        Dear {application.user.name},

        You have been shortlisted for the position of {application.job.title}.
        We will contact you with the next steps.

        Best regards,
        The TalentTrade Team
        """
        send_email(subject, recipients, text_body)

        flash('The application has been reviewed and the user has been shortlisted.', 'success')
    else:
        application.status = 'rejected'
        db.session.commit()
        flash('The application has been reviewed and the user has not been shortlisted.', 'danger')

    return redirect(url_for('admin.dashboard'))


@application_bp.route('/shortlisted_applications/<int:job_id>', methods=['GET'])
@login_required
def view_shortlisted_applications(job_id):
    # Get the job object
    job = Job.query.get_or_404(job_id)

    # Get the shortlisted applications for the job
    shortlisted_applications = Application.query.filter(
        Application.status == 'accepted',
        Application.job_id == job_id
    ).all()

    # Render the template with the shortlisted applications
    return render_template('application/shortlisted_applications.html',
                           applications=shortlisted_applications,
                           job=job)

@application_bp.route('/job/<int:job_id>/apply', methods=['GET'])
@login_required
def application_form(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('application/application_form.html', job=job)


@application_bp.route('/application/<int:application_id>/', methods=['GET'])
@login_required
def application_detail(application_id):
    # Fetch the application by ID
    application = Application.query.get_or_404(application_id)

    return render_template('application/application_detail.html', application=application)


@application_bp.route('/job/<int:job_id>/apply', methods=['POST'])
@login_required
def submit_application(job_id):
    cover_letter = request.form['cover_letter']
    expected_rate = request.form['expected_rate']
    
    response, status = application_service.ApplicationService.submit_application(
        job_id, cover_letter, expected_rate)
    
    match status:
        case 200:
            flash('Application submitted successfully!', 'success')
        case 400:
            flash(f'{response}\
                \nBad request. Please check your input and try again.', 'danger')
        case 500:
            flash(f'{response}\
                \nInternal server error. Please try again later.',
                'danger')
        case _:
            flash(f'{response}\
                \nUnknown error occurred. Please try again later.', 'danger')
    return redirect(url_for('job.job_detail', job_id=job_id))
