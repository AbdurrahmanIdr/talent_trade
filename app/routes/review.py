from flask import Blueprint, render_template, redirect, url_for, request
from app.models.review import Review
from app.extensions import db

bp = Blueprint('reviews', __name__, template_folder='app/templates/')


@bp.route('/reviews', methods=['GET'])
def review_list():
    reviews = Review.query.all()
    return render_template('review/review_list.html', reviews=reviews)


@bp.route('/review/new', methods=['GET', 'POST'])
def new_review():
    
    return render_template('review/review_form.html')
