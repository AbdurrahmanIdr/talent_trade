from app.models import Payment
from app import db


class PaymentService:
    def create_payment(self, amount, user_id, job_id):
        new_payment = Payment(amount=amount, user_id=user_id, job_id=job_id)

        db.session.add(new_payment)
        db.session.commit()

        return new_payment

    def get_payments_by_user(self, user_id):
        return Payment.query.filter_by(user_id=user_id).all()

    def get_payment_details(self, payment_id):
        return Payment.query.get(payment_id)
