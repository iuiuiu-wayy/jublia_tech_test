# jublia_tech_test
This app is develooped for Technical test of Jublia recruitment process.
To run this app, a few changes should be added to config.py file.
The required changes is to connect email so that the app can send email automatically.
Dockerfile and docker-compose.yml files are used to create container for this app to run.

To run the app, follow the instructions below:
1. navigate to the app directory
2. Add config.py file
code:

```
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres' # 'postgresql://postgres:project@localhost/JubliaDB'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'email@gmail.com'        <<<<< add email
    MAIL_PASSWORD = 'password'               <<<<< add password
    MAIL_DEFAULT_SENDER = 'email@gmail.com'  <<<<< add email
    DEBUG = True
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    CELERY_BROKER_URL='redis://redis:6379'
    CELERY_RESULT_BACKEND='redis://redis:6379'
    TIMEZONE = 'Singapore'
 ```
    
4. Run the following code to create container:

  docker-compose build
  
  docker-compose up
  

3. The app is accessible through browser 127.0.0.1:5000/ (recommended using google chrome)

The app provide user interface. User first need to add email address to the database by typing the email address and click on add email address.
The changes can be seen after clickon on refress button.
To send email, user need to fill up the form for email subject, content, date, and time for the app to send the email.
The task then is submitted and the process can be seen by clicking on refresh button again.
App will update the status when the email is sent.
