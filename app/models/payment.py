"""Payment model"""
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=False)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='pending')  # 'pending', 'completed', 'failed'
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # Relationships
    client = relationship('User', foreign_keys=[client_id], back_populates='payments_made')
    freelancer = relationship('User', foreign_keys=[freelancer_id], back_populates='payments_received')
    job = relationship('Job', foreign_keys=[job_id], back_populates='payment')

    def __repr__(self) -> str:
        return f'<Payment {self.id}>'

