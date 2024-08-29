from flask import (
    Blueprint, render_template, redirect,
    url_for, flash,  request)

from flask_login import current_user, login_required

from app.extensions import db
from app.models import Job, Application, Message
from app.services import JobService

job_bp = Blueprint('job', __name__)


@job_bp.route('/jobs', methods=['GET'])
@login_required
def job_listings():
    jobs = Job.query.all()
    return render_template('job/job_listings.html', jobs=jobs)


@job_bp.route('/user_jobs', methods=['GET'])
@login_required
def user_job_listings():
    if current_user.role == 'client':
        jobs = current_user.posted_jobs
        
    elif current_user.role == 'freelancer':
        applications = Application.query.filter(Application.freelancer==current_user).all()
        jobs = [application.job for application in applications]
        
    else:
        jobs = []

    return render_template('job/job_listings.html', jobs=jobs)


@job_bp.route('/job/<int:job_id>', methods=['GET'])
@login_required
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/job_detail.html', job=job)


@job_bp.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']

        response, status = JobService.create_job(
            title=title, description=description,
            budget=budget)

        match status:
            case 200:
                flash('Job created successfully!', 'success')
                return redirect(url_for('job.user_job_listings'))

            case 400:
                flash('Something went wrong!', 'danger')

    return render_template('job/create_job.html')


@job_bp.route('/job/update/<int:job_id>', methods=['GET', 'POST'])
@login_required
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if job.client_id != current_user.id:
        flash(
            'You are not authorized to update this job.',
            'danger')
        return redirect(url_for('job.job_detail', job_id=job_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        budget = request.form.get('budget')

        response, status = JobService.update_job(
            job_id, title, description, budget)

        match status:
            case 200:
                flash(
                    response.get('message', 'Job updated successfully!'),
                    'success')

            case 401:
                flash(
                    'You are not authorized to update this job.',
                    'danger')

        return redirect(url_for('job.job_detail', job_id=job_id))

    return render_template('job/edit_job.html', job=job)


@job_bp.route('/job/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    response, status = JobService.delete_job(job_id)
    match status:
        case 200:
            user_id = current_user.id
            flash(response, 'success')
            return redirect(url_for(
                'job.user_job_listings', user_id=user_id))

        case 401:
            flash(response, 'danger')

        case 500:
            flash(response, 'danger')

    return redirect(url_for('job.job_listings', jobs=None))


@job_bp.route('/applications/<int:job_id>', methods=['GET'])
@login_required
def view_applications(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.client_id == current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('job.job_detail', job_id=job_id))

    applications = Application.query.filter_by(job_id=job_id).all()
    return render_template('application/shortlisted_applications.html', applications=applications, job=job)


@job_bp.route('/update_application_status/<int:application_id>/<string:status>', methods=['GET'])
@login_required
def update_status(application_id, status):
    if status not in ['accepted', 'rejected']:
        flash('Invalid status!', 'danger')
        return redirect(url_for('job.view_applications', job_id=job.id))

    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)

    if job.client_id != current_user.id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('job.view_applications', job_id=job.id))

    application.status = status
    db.session.commit()

    # Notify the freelancer via in-app message
    freelancer = application.freelancer
    if status == 'accepted':
        content = f"Congratulations! Your application for the job '{job.title}' has been accepted. Please proceed with the project or await further instructions from the client."
    elif status == 'rejected':
        content = f"We regret to inform you that your application for the job '{job.title}' has been rejected. Please feel free to apply for other jobs."

    message = Message(
        sender_id=current_user.id,
        recipient_id=freelancer.id,
        content=content
    )
    db.session.add(message)
    db.session.commit()

    flash(f'Application {status} successfully!', 'success')
    return redirect(url_for('job.view_applications', job_id=job.id))
