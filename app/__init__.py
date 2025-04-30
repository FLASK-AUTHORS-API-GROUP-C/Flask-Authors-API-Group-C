from flask import Flask
from app.extensions import db,migrate,jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.company.comp_controller import companies
from app.controllers.books.book_controller import books
from flask import Blueprint,request,jsonify



# application factory function.
def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')
# initialising against our app instance
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    # bcrypt.init_app(app)
  

    #Registering models
    from app.models.author_model import Author
    from app.models.company_model import Company
    from app.models.book_model import Book
   

    # registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(companies)
    app.register_blueprint(books)


    
    # index route(first route)
    @app.route('/')
    def home():
        return "hello"
       
    return app  