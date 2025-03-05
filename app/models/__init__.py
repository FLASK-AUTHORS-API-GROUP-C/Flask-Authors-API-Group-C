from flask import Flask
from app.extensions import db,migrate


# application factory function.
def create_app():

    app = Flask(_name_)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app,db)
  

    #Registering models
    from app.models.author_model import Author
    from app.models.book_model import Book
    from app.models.company_model import Company


    # index route(first route)
    @app.route('/')
    def home():
        return "hello"
      
      return app
      