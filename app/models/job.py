"""Job model"""
from datetime import datetime
from sqlalchemy import String, Integer, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class Job(db.Model):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[int] = mapped_column(Text, nullable=False)
    budget: Mapped[int] = mapped_column(Float, nullable=False)
    status: Mapped[int] = mapped_column(String(50), nullable=False, default='open')
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    created_at: Mapped[int] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[int] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationship
    client = relationship('User', foreign_keys=[client_id], back_populates='posted_jobs')
    freelancer = relationship('User', foreign_keys=[freelancer_id], back_populates='freelancer_jobs')
    applications = relationship('Application', foreign_keys='Application.job_id', back_populates='job')
    payment = relationship('Payment', foreign_keys='Payment.job_id', uselist=False, back_populates='job')
    review = relationship('Review', foreign_keys='Review.job_id', uselist=False, back_populates='job')

    def __repr__(self) -> str:
        return f'<Job {self.title}>'
