from app.extensions import db
from datetime import datetime

# Book class.
class Book(db.Model):

    __tablename__ ="Books"
    title =db.Column(db.String(255),nullable=False)
    image = db.Column(db.String(255),nullable=True) 
    id = db.Column(db.Integer,primary_key=True)
    description =db.Column(db.String(200),nullable =False)
    no_of_pages =db.Column(db.Integer,nullable=False)
    isbn =db.Column(db.String(30),nullable=False)
    publication_date =db.Column(db.Date,nullable=False)
    price = db.Column(db.String(50) ,nullable=False)
    created_at =db.Column(db.DateTime,default = datetime.now())
    updated_at = db.Column(db.DateTime,onupdate =datetime.now())


    def __init__(self,id,title,price,image,publication_date,description,isbn, no_of_pages): 
        self.id =id
        self.title =title
        self.price =price
        self.image =image
        self.publication_date =publication_date
        self.description = description
        self.no_of_paages = no_of_pages
        self.isbn = isbn
        
                 


    

 