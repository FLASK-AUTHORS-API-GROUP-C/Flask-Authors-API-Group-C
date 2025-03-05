from app.extensions import db
from datetime import datetime


# adding a constructor.
class Company(db.Model):

    __tablename__="Company"
    name =db.Column(db.String(50),nullable =False)
    id = db.Column(db.Integer,primary_key=True)
    origin =db.Column(db.String(50),nullable=False)
    description =db.Column(db.String(255),nullable=False)
    email =db.Column(db.String(50),nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, onupdate =datetime.now())


    def __init__(self, id,name,origin,email,description,created_at,updated_at): 
                self.id =id
                self.name = name
                self.origin = origin
                self.email =email
                self.description = description
                self.created_at= created_at
                self.updated_at = updated_at
            
                 





