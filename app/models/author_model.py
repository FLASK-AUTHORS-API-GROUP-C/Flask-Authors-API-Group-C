
from app.extensions import db # Every word accessed after the db starts with a capital letter eg db.C,R,T,D,F
from datetime import datetime

class Author(db.Model):        # The datatype and word limit should be defined eg string(30)
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True,nullable = False)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(20),nullable=False)
    biography = db.Column(db.String(20),nullable=True)
    contact = db.Column(db.String(30),nullable=False,unique = True)
    email= db.Column(db.String(20),nullable=False, unique=True)
    password= db.Column(db.String(250),nullable=False)
    created_at = db.Column(db.DateTime, default= datetime.now)
    updated_at = db.Column(db.DateTime,onupdate= datetime.now) 
    
    def __init__(self,first_name,last_name,contact,email,password, biography):
        super(Author,self).__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password= password
        self.biography = biography
        self.book = []

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
    def add_book(self,book):
        self.book.append(book)
    


