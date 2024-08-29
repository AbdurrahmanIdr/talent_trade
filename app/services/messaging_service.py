from app.models import Message
from app import db

class MessagingService:
    def send_message(self, content, sender_id, recipient_id):
        new_message = Message(content=content, sender_id=sender_id, recipient_id=recipient_id)

        db.session.add(new_message)
        db.session.commit()

        return new_message

    def get_chat_history(self, user_id, recipient_id):
        messages = Message.query.filter(
            (Message.sender_id == user_id) & (Message.recipient_id == recipient_id) |
            (Message.sender_id == recipient_id) & (Message.recipient_id == user_id)
        ).order_by(Message.timestamp.asc()).all()

        return messages
