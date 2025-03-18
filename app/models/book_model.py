
     # Attributes should be related to the class mentioned
from app.extensions import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = "books"
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(30),nullable=False)
    price= db.Column(db.String(20),nullable=False)
    description= db.Column(db.String(50),nullable=False) 
    image = db.Column(db.String(50),nullable=True)
    publication_date = db.Column(db.Date,nullable = False)
    isbn = db.Column(db.String(30),nullable=True,unique=True)
    pages = db.Column(db.String(30),nullable=False)
    genre = db.Column(db.String(50),nullable=False)
    unit_price = db.Column(db.String(20),nullable=False)
    author_id =db.Column(db.Integer,db.ForeignKey("authors.id"))
    company_id =db.Column(db.Integer,db.ForeignKey("companies.id"))
    author = db.relationship('Author',backref = 'books')
    company = db.relationship('Company',backref = 'books')
    created_at = db.Column(db.DateTime, default= datetime.now())
    updated_at = db.Column(db.DateTime,onupdate= datetime.now()) 
    

    def __init__(self,title,price,description,image,pages,unit_price):

          self.title= title
          self.price = price
          self.description = description
          self.image = image
          self.pages= pages
          self.unit_price = unit_price

