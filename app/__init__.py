from flask import Flask
from app.extensions import db,migrate,bcrypt,jwt
from app.controllers.auth.auth_controller import auth
from flask import Blueprint,request,jsonify


# application factory function.
def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    # bcrypt.init_app(app)
  

    #Registering models
    from app.models.author_model import Author
    from app.models.book_model import Book
    from app.models.company_model import Company


    # registering blue prints
    app.register_blueprint(auth)
    app.register_blueprint(Company)


    auth = Blueprint('auth', __name__,url_prefix='/api/v1/auth')
    Company = Blueprint("company",__name__,url_prefix='/api/v1/company')


    # index route(first route)
    @app.route('/')
    def home():
        return "hello"
       
    return app  