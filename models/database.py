from . import db
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Sequence, ForeignKey, UnicodeText
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Emails(Base):
    __tablename__ = 'emails'
    event_id = Column(Integer, primary_key=True)
    email_subject = Column(UnicodeText)
    email_content = Column(UnicodeText)
    timestamp = Column(DateTime(timezone=True))
    celery_id = Column(String)
    status = Column(String)


class Recipient_emails(Base):
    __tablename__ = 'recipient_emails'
    email_address = Column(String, unique=True, primary_key=True)

Base.metadata.create_all(db.engine)
Session = sessionmaker(bind=db.engine)


