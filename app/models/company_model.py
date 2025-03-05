from app.extensions import db
from datetime import datetime
class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10),nullable=False)
    origin = db.Column(db.String(10),nullable=False)
    description = db.Column(db.String(50),nullable=False) 
    unit_price = db.Column(db.String(10),nullable=False)
    image = db.Column(db.String(50),nullable=True)
    bio = db.Column(db.String(30),nullable=False)
    author_id =db.Column(db.Integer,db.ForeignKey("authors.id"))

    def __init__(self,name,origin,description,unit_price,image,Bio):         
        self.name = name
        self.origin = origin
        self.description = description
        self.unit_price = unit_price
        self.image = image
        self.Bio = Bio

        
    
