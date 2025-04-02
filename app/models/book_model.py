from app.extensions import db
from datetime import datetime

# Book class.
class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(500), nullable=False)
    no_of_pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(30), unique=True, nullable=True)
    publication_date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Fixed float issue
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.author_id", ondelete="CASCADE"))
    company_id = db.Column(db.Integer, db.ForeignKey("companies.company_id", ondelete="SET NULL"))

    author = db.relationship("Author", back_populates="books")
    company = db.relationship("Company", back_populates="books")


    def __init__(self,book_id,title,price,image,publication_date,description,isbn, no_of_pages,created_at,updated_at,author_id,company_id,author,company): 
        super(Book,self).__init__()
        self.book_id =book_id
        self.title =title
        self.price =price
        self.image =image
        self.publication_date =publication_date
        self.description = description
        self.no_of_paages = no_of_pages
        self.isbn = isbn
        self.created_at = created_at
        self.updated_at = updated_at
        self.author_id = author_id
        self.company_id = company_id
        self.company = company
        self.author = author

    def __repr__(self):
        return f"Book { self.title }"
        
                 


    

 
