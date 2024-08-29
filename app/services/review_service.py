from app.models.review import Review
from app.extensions import db


class ReviewService:
    @staticmethod
    def create_review(job_id, user_id, rating, comment):
        review = Review(job_id=job_id, user_id=user_id, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
        return {'message': 'Review created successfully'}, 201
