from app.models import User
from app.extensions import db

from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class AuthService:
    @staticmethod
    def register_user(username, email, password, role, fullname):
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already registered'}, 400

        try:
            user = User()
            user.username = username.lower()
            user.email = str(email).lower()
            user.set_password(password)
            user.full_name = fullname
            user.bio = ''
            user.role = role

            db.session.add(user)
            db.session.commit()

            return {
                'message': 'User registered successfully'
            }, 201
            
        except SQLAlchemyError as se:
            return {
                'message': se
            }, 401

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return {
                'message': 'Login successful!',
                'user_id': user.id,
            }, 200
        return {'error': 'Invalid credentials'}, 400

    @staticmethod
    def reset_password(user, new_password):
        user.set_password(new_password)
        db.session.commit()
        return {'message': 'Password updated successfully'}, 200
