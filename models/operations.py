import email
from flask import session
from sqlalchemy import desc
from .database import Session, Emails, Recipient_emails

session = Session()

def get_recipient_emails():
    recipients = session.query(Recipient_emails.email_address).all()
    return list( *zip(*recipients) )

def get_recent_task(n=5):
    emails = session.query(Emails.email_subject, Emails.status, Emails.timestamp).order_by(Emails.event_id.desc()).limit(n).all()
    return emails

def add_new_recipient(email):
    new_recipient = Recipient_emails(email_address=email)
    session.add(new_recipient)
    session.commit()