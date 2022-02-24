import pytz
import datetime
from flask import request, make_response
import time
from flask_mail import  Message

def init_app(app, mail, celery):
    LOCAL_TIMEZONE = pytz.timezone(app.config['TIMEZONE'])
    
    @celery.task()
    def send_mail(email_subject, email_content, email_timestamp, email_id): 
        print('task starting')

        time_now = datetime.datetime.now().astimezone(LOCAL_TIMEZONE)
        time_input = datetime.datetime.strptime(email_timestamp, '%Y-%m-%d %H:%M:%S%z').astimezone(LOCAL_TIMEZONE)
        print(time_now, time_input)

        with app.app_context():
            from models.database import Emails, Session, Recipient_emails
        
        if time_now > time_input:
            session = Session()
            email = session.query(Emails).filter_by(event_id=email_id).all()[0]
            email.status = "FAIL"

        else:
            time.sleep((time_input - time_now).seconds)
            session = Session()
            recipients = session.query(Recipient_emails.email_address).all()
            msg = Message(
                email_subject,
                sender= 'wahyu.amanullah27@gmail.com',
                recipients = list( *zip(*recipients) ) 
            )
            msg.body = email_content
            mail.send(msg)
            email = session.query(Emails).filter_by(event_id=email_id).all()[0]
            email.status = "SUCCESS"

        # session = Session()
        session.add(email)
        session.commit()
        print('task finished')


    @app.route("/")
    def home():
        return "Hello World!"
    
    @app.route('/save_emails', methods=['POST'])  
    def save_emails():
        email_subject = request.args.get('email_subject')
        email_content = request.args.get('email_content')
        email_timestamp = request.args.get('timestamp') + '+0800'
        print(email_subject, email_content, email_timestamp)
        with app.app_context():
            from models.database import Emails, Session
        email= Emails(email_subject = email_subject, email_content=email_content, timestamp=email_timestamp, celery_id='-', status="PENDING")
        session = Session()
        session.add(email)
        session.commit()
        # time_now = datetime.datetime
        async_task = send_mail.delay(email_subject, email_content, email_timestamp, email.event_id)
        
        # task = Tasks(status='PENDING', celery_id=async_task.id)
        # email= Emails(email_subject = email_subject, email_content=email_content, timestamp=email_timestamp, celery_id=async_task.id, status="PENDING")
        email.celery_id = async_task.id
        # session = Session()
        session.add(email)
        session.commit()
        # from run import send_email
        # job = q.enqueue(send_email)
        # print(f"Task ({job.id}) added to queue at {job.enqueued_at}")
        return make_response(
            'Test worked!',
            200,
        )
    
    @app.route('/add_recipient_email', methods=['POST'])
    def add_recipient_email():
        email_address = request.args.get('email_address')
        with app.app_context():
            from models.database import Recipient_emails, Session
        
        add_email = Recipient_emails(email_address=email_address)
        session = Session()
        session.add(add_email)
        session.commit()
        return make_response(
            'Test worked!',
            200
        )

