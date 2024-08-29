from flask_login import current_user

from app.models import Job
from app.extensions import db


class JobService:
    @staticmethod
    def create_job(title, description, budget):
        if not title or not description or not budget:
            return {'error': 'Missing required fields'}, 400

        new_job = Job(title=title, description=description, budget=budget)
        new_job.client_id = current_user.id

        db.session.add(new_job)
        db.session.commit()

        return new_job, 200

    @staticmethod
    def update_job(job_id, title=None, description=None, budget=None):
        job = Job.query.get_or_404(job_id)

        if job.client_id != current_user.id:
            return {'You are not authorized to update this job.'}, 401

        if title is not None:
            job.title = title
        if description is not None:
            job.description = description
        if budget is not None:
            job.budget = budget

        db.session.commit()
        return {'message': 'Job updated!'}, 200

    @staticmethod
    def delete_job(job_id):
        job = Job.query.get(job_id)

        if job.client_id != current_user.id:
            return 'You are not authorized to delete this job.', 401

        if job:
            db.session.delete(job)
            db.session.commit()
            return 'Job deleted successfully!', 200

        return 'Something went wrong!', 500

    @staticmethod
    def get_jobs_by_user(user_id):
        jobs = Job.query.filter(Job.client.id == user_id).all()

        if not jobs:
            return {'error': 'No jobs found for this user.'}, 400

        return {'jobs': jobs}, 200
