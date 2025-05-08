from flask import Flask
from app.extensions import db,migrate,jwt
from app.controllers.auth_controller import auth
from app.controllers.user.user_controller import users
from app.controllers.book_controller import book

#application factory function
def create_app():

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    

    #Registering models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book

    #registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(book)

 
    #index route
    @app.route("/") #the decorator must be at the top 
    def landing():
        return "hi how are you"

    return app

  