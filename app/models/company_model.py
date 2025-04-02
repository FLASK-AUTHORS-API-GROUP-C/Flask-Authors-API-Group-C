from app.extensions import db
from datetime import datetime


# adding a constructor.
class Company(db.Model):
    __tablename__ = "companies"

    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    origin = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    # Relationships
    authors = db.relationship("Author", back_populates="company")  # A company has many authors
    books = db.relationship("Book", back_populates="company") 

    def __init__(self, company_id,name,origin,email,description,created_at,updated_at): 
                super(Company,self).__init__()
                self.company_id =company_id
                self.name = name
                self.origin = origin
                self.email =email
                self.description = description
                self.created_at= created_at
                self.updated_at = updated_at
            
                 





