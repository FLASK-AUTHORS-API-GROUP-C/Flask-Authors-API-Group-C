from flask import Flask
from app.extensions import db,migrate
from app.controllers.auth_controllers import auth

#application factory function
def create_app():

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app,db)
    

    #Registering models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book

    #registering blueprints
    app.register_blueprint(auth)

 
    #index route
    @app.route("/") #the decorator must be at the top 
    def landing():
        return "hi how are you"

    return app

  