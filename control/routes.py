from flask import request, make_response
import pytz
import datetime, time
from flask_mail import Message

def init_routes(app, mail, celery):
    LOCAL_TIMEZONE = pytz.timezone(app.config['TIMEZONE'])
    
    @celery.task()
    def send_mail(email_subject, email_content, email_timestamp, email_id): 
        print('task starting')

        time_now = datetime.datetime.now().astimezone(LOCAL_TIMEZONE)
        time_input = datetime.datetime.strptime(email_timestamp, '%Y-%m-%d %H:%M:%S%z').astimezone(LOCAL_TIMEZONE)
        print(time_now, time_input)

        with app.app_context():
            from models.operations import assign_email_status, get_email_recipient
        if time_now > time_input:
            status = "FAIL"

        else:
            time.sleep((time_input - time_now).seconds)
            recipients = get_email_recipient
            msg = Message(
                email_subject,
                sender= 'wahyu.amanullah27@gmail.com',
                recipients = recipients
            )
            msg.body = email_content
            status = "SUCCESS"
        assign_email_status(email_id, status)
        print('task finished')

    @app.route("/")
    def home():
        return "Hello World!"
    
    @app.route('/save_emails', methods=['POST'])  
    def save_emails():
        email_subject = request.form.get('email_subject')
        email_content = request.form.get('email_content')
        email_timestamp = request.form.get('timestamp') + '+0800'
        print(email_subject, email_content, email_timestamp)
        with app.app_context():
            from models.operations import new_emails, new_email_celery_id
        
        email_id = new_emails(email_subject = email_subject, email_content=email_content, timestamp=email_timestamp, celery_id='-', status="PENDING")
        async_task = send_mail.delay(email_subject, email_content, email_timestamp, email_id)
        new_email_celery_id(email_id, async_task.id)
        return make_response(
            'Test worked!',
            200,
        )
    @app.route('/add_recipient_email', methods=['POST', 'GET'])
    def add_recipient_email():
        email_address = request.form.get('email_address')
        print('from endpoint   ',email_address)
        with app.app_context():
            from models.operations import add_new_recipient
        
        add_new_recipient(email_address)
        return make_response(
            'Test worked!',
            200
        )