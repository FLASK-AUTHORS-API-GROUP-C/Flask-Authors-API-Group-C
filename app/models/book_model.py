from app.extensions import db
from datetime import datetime


class Book(db.Model):

    # The tabel name
    __tablename__ = 'book'
   
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(20), nullable = True)
    pages = db.Column(db.Integer, nullable = False)
    publication_date = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, default = datetime.now())


    def __init__(self, id, title, price, description, image, pages, publication_date,created_at,updated_at  ):

        self.id = id
        self.title = title
        self.price = price
        self.description = description
        self.image= image
        self.pages= pages
        self.publication_date = publication_date
        self.created_at = created_at
        self.updated_at = updated_at
  
        






 