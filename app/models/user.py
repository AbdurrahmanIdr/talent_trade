"""User model"""
from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(50))  # 'freelancer', 'client', 'admin'
    bio: Mapped[str] = mapped_column(Text)
    profile_picture: Mapped[str] = mapped_column(String(200), default='default.png')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())

    # Jobs posted by this user as a client
    posted_jobs = relationship('Job', foreign_keys='Job.client_id', back_populates='client')
    # Jobs undertaken by this user as a freelancer
    freelancer_jobs = relationship('Job', foreign_keys='Job.freelancer_id', back_populates='freelancer')

    # Reviews given by this user (as a client)
    reviews_given = relationship('Review', foreign_keys='Review.client_id', back_populates='client')
    # Reviews received by this user (as a freelancer)
    reviews_received = relationship('Review', foreign_keys='Review.freelancer_id', back_populates='freelancer')

    # Payments made by this user (as a client)
    payments_made = relationship('Payment', foreign_keys='Payment.client_id', back_populates='client')
    # Payments received by this user (as a freelancer)
    payments_received = relationship('Payment', foreign_keys='Payment.freelancer_id', back_populates='freelancer')

    # Applications submitted by this user as a freelancer
    applications = relationship('Application', foreign_keys='Application.freelancer_id', back_populates='freelancer')

    messages_sent = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)

    def is_active(self):
        """Returns True, as all users are active by default."""
        return True

    def is_authenticated(self):
        """Returns True if the user is authenticated."""
        return True

    def is_anonymous(self):
        """Returns False, as anonymous users aren't supported."""
        return False

    def __repr__(self) -> str:
        return f'<User {self.username}>'
