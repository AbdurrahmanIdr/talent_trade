"""Application Model"""
from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class ApplicationStatusEnum(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class Application(db.Model):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=False)
    cover_letter: Mapped[str] = mapped_column(Text)
    expected_rate: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default=ApplicationStatusEnum.PENDING)
    applied_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    freelancer = relationship('User', foreign_keys=[freelancer_id], back_populates='applications')
    job = relationship('Job', foreign_keys=[job_id], back_populates='applications')
    
    __table_args__ = (
        db.UniqueConstraint('job_id', 'freelancer_id', name='unique_application'),
    )

    def __repr__(self) -> str:
        return f'<Application: {self.id}>'
