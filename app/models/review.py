"""Review model"""
from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=False)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 5
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    review_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    client = relationship('User', foreign_keys=[client_id], back_populates='reviews_given')
    freelancer = relationship('User', foreign_keys=[freelancer_id], back_populates='reviews_received')
    job = relationship('Job', foreign_keys=[job_id], back_populates='review')

    def __repr__(self) -> str:
        return f'<Review {self.id}>'
