from flask import (
    Blueprint, render_template,
    redirect, url_for, flash, request, jsonify)
from flask_login import login_required, current_user


from app import db
from app.models import Payment

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/make_payment', methods=['POST'])
def make_payment():
    amount = request.form['amount']
    user_id = request.form['user_id']
    job_id = request.form['job_id']

    new_payment = Payment(amount=amount, user_id=user_id, job_id=job_id)
    db.session.add(new_payment)
    db.session.commit()

    flash('Payment successful!', 'success')
    return redirect(url_for('job.job_listings'))


@payment_bp.route('/payment_history', methods=['GET'])
def payment_history():
    payments = Payment.query.all()
    return render_template('payment/payment_history.html', payments=payments)


@payment_bp.route('/payments', methods=['GET'])
@login_required
def get_payments():
    user_id = current_user.id
    payments = Payment.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': pay.id,
        'amount': pay.amount,
        'status': pay.status
    } for pay in payments]), 200


@payment_bp.route('/payments', methods=['POST'])
@login_required
def create_payment():
    data = request.get_json()
    amount = data.get('amount')
    user_id = current_user.id

    payment = Payment(user_id=user_id, amount=amount)
    db.session.add(payment)
    db.session.commit()

    return jsonify({'message': 'Payment created successfully'}), 201
