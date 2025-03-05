from app.extensions import db
from datetime import datetime




class Company(db.Model):
    #Adding the name of the table
    __tablename__  = 'company'

    # Adding a constructor
    
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    origin = db.Column(db.String(20), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    created_at= db.Column(db.DateTime, default = datetime.now())
    updated_at = db.Column(db.DateTime, default = datetime.now())
    

    def __init__(self,name, id, origin, description,created_at, updated_at):
        self.name = name
        self.id = id
        self.origin = origin
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        

 