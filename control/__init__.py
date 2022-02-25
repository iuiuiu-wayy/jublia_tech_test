from .routes import init_routes

def init_app(app, mail, celery):
    init_routes(app, mail, celery)


    

