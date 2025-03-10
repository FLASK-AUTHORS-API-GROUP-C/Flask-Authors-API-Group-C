from app.extensions import db
from datetime import datetime


class Book(db.Model):

    # The tabel name
    __tablename__ = 'books'
   
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String(20), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(200), nullable = False)
    image = db.Column(db.String(20), nullable = True)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))
    company_id = db.Column(db.Integer,db.ForeignKey('company.id'))
    author = db.relationship('Author',backref = 'books')
    company = db.relationship('Company',backref = 'books')
    pages = db.Column(db.Integer, nullable = False)
    publication_date = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, default = datetime.now())


    def __init__(self, id, title, price, description, image, pages, publication_date,created_at,updated_at,company_id,author_id,company,author  ):

        self.id = id
        self.title = title
        self.price = price
        self.description = description
        self.image= image
        self.pages= pages
        self.publication_date = publication_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.company_id = company_id
        self.author_id = author_id
        self.company = company
        self.author = author

        
  
        






 