from flask_mail import Message
from app.extensions import mail


def send_email(subject, recipient, body, html=None, sender="no-reply@talenttrade.com"):
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body
    if html:
        msg.html = html
    mail.send(msg)

