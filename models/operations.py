from flask import session
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

def new_emails(email_subject, email_content, timestamp, celery_id, status):
    email = Emails(email_subject = email_subject, email_content=email_content, timestamp=timestamp, celery_id='-', status="PENDING")
    session.add(email)
    session.commit()
    return email.event_id

def new_email_celery_id(email_id, celery_id):
    email = session.query(Emails).filter_by(event_id=email_id).all()[0]
    email.celery_id = celery_id
    session.add(email)
    session.commit()
    return email.event_id

def assign_email_status(email_id, status):
    email = session.query(Emails).filter_by(event_id=email_id).all()[0]
    email.status = status
    session.add(email)
    session.commit()
    return email.event_id

def get_email_recipient():
    recipients = session.query(Recipient_emails.email_address).all()
    list_recipients = list( *zip(*recipients) ) 
    return list_recipients