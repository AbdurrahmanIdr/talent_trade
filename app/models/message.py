"""Message model"""
from datetime import datetime
from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class Message(db.Model):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=False)

    sender = relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    recipient = relationship('User', foreign_keys=[receiver_id], back_populates='messages_received')
    job = relationship('Job', foreign_keys=[job_id], back_populates='messages')

    def __repr__(self):
        return f"<Message {self.content[:20]}>"
