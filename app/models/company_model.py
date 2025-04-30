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

    def __init__(self,name,origin,description,email): 
                super(Company,self).__init__()
                
                self.name = name
                self.origin = origin
                self.description = description
                self.email = email

    def get_full_name(self):
        return f"{self.name} ({self.origin})"
                

            
                 





