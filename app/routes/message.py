from flask import (
    render_template, redirect, url_for,
    Blueprint, request, flash, abort
)
from flask_login import current_user, login_required
from app.models.message import Message
from app.extensions import db
from app.models import User
from datetime import datetime

message_bp = Blueprint('message', __name__)


@message_bp.route('/inbox')
@login_required
def inbox():
    # Retrieve unique conversations involving the current user
    conversations = db.session.query(
        Message.sender_id, Message.recipient_id, db.func.max(Message.sent_at).label('last_sent_at')
    ).filter(
        (Message.sender_id == current_user.id) | (Message.recipient_id == current_user.id)
    ).group_by(
        db.case(
            (Message.sender_id < Message.recipient_id, Message.sender_id),
            else_=Message.recipient_id
        ),
        db.case(
            (Message.sender_id < Message.recipient_id, Message.recipient_id),
            else_=Message.sender_id
        )
    ).order_by(
        db.func.max(Message.sent_at).desc()
    ).distinct().all()
    
    # Prepare conversation details with the last message and other user info
    conversation_details = []
    for conversation in conversations:
        other_user_id = conversation.recipient_id if conversation.sender_id == current_user.id else conversation.sender_id
        other_user = User.query.get_or_404(other_user_id)
        last_message = Message.query.filter(
            (Message.sender_id == current_user.id) & (Message.recipient_id == other_user_id) |
            (Message.sender_id == other_user_id) & (Message.recipient_id == current_user.id)
        ).order_by(Message.sent_at.desc()).first()
        conversation_details.append({
            'user': other_user,
            'last_message': last_message
        })

    return render_template('message/inbox.html', conversations=conversation_details)


@message_bp.route('/chat/<int:other_user_id>')
@login_required
def chat(other_user_id):
    # Retrieve chat messages between the current user and the other user
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.sent_at.desc()).all()  # Changed to desc()

    # Reverse the list of messages
    messages = list(reversed(messages))

    # Retrieve the other user's information
    other_user = User.query.get_or_404(other_user_id)

    # Mark messages as read
    for message in messages:
        if message.recipient_id == current_user.id:
            message.read = True
    db.session.commit()

    return render_template('message/chat.html', messages=messages, other_user=other_user)


@message_bp.route('/send_message/<int:recipient_id>', methods=['POST'])
@login_required
def send_message(recipient_id):
    content = request.form.get('body')

    if not content:
        flash('Message content cannot be empty!', 'danger')
        return redirect(url_for('message.chat', other_user_id=recipient_id))

    new_message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()

    flash('Message sent successfully!', 'success')
    return redirect(url_for('message.chat', other_user_id=recipient_id))


@message_bp.route('/messages/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)

    if message.receiver_id != current_user.id and message.sender_id != current_user.id:
        abort(403)

    if not message.is_read:
        message.is_read = True
        db.session.commit()

    return render_template('message/view_message.html', message=message)
