from flask_mail import Message, BadHeaderError
from smtplib import SMTPResponseException
from app.extensions import mail


def recieve_email(subject, sender, body, html=None, recipient="deveoptest01@gmail.com"):
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = body
    if html:
        msg.html = html
        
    try:
        mail.send(msg)
        return 'success', 200
        
    except BadHeaderError:
    # Catch bad header errors, e.g. when the sender or recipient is invalid
        return 'Bad header error', 400

    except ConnectionRefusedError:
        # Catch connection refused errors, e.g. when the mail server is down
        return 'Mail server connection refused', 500

    except SMTPResponseException as e:
        # Catch SMTP response exceptions, e.g. when the mail server returns an error
        return f'SMTP error: {e.smtp_code} {e.smtp_error}', 500

    except Exception as e:
        # Catch all other exceptions, e.g. when there's a problem with the email content
        return f'Error sending email: {str(e)}', 400 

