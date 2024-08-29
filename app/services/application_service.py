from app.extensions import db
from app.models import Application, Job
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask_login import current_user


class ApplicationService:
    @staticmethod
    def submit_application(job_id, cover_letter, expected_rate):
        try:
            # Check if the freelancer has already applied for the job
            existing_app = Application.query.filter(
                Application.job_id==job_id and Application.freelancer_id==current_user.id).first()

            if existing_app:
                raise ValueError('You have already applied for this job!')

            new_app = Application()
            new_app.job_id = job_id
            new_app.freelancer_id = current_user.id
            new_app.cover_letter = cover_letter
            new_app.expected_rate = expected_rate

            db.session.add(new_app)
            db.session.commit()
            return 'Application submitted successfully!', 200
        
        except ValueError as e:
            # Handle duplicate application error
            return f'ValueError: {e}', 400
        except IntegrityError as e:
            # Handle database integrity errors (e.g., duplicate application)
            return f'IntegrityError: {e}', 400
        except SQLAlchemyError as e:
            # Handle SQLAlchemy-specific errors (e.g., database connection issues)
            return f'SQLAlchemyError: {e}', 500
        except Exception as e:
            # Catch all other exceptions (e.g., unexpected errors)
            return f'Error: {e}', 500
