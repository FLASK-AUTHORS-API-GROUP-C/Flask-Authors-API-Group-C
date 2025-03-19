from app.extensions import db
from datetime import datetime  # The extension for updating the date
class Author(db.Model):
        __tablename__ = 'authors'
   

        id = db.Column(db.Integer, primary_key=True, nullable = False)
        first_name = db.Column(db.String(100), nullable = False)
        last_name = db.Column(db.String(100), nullable = False)
        author_contact = db.Column(db.String(100), nullable = False)
        email_addresss = db.Column(db.String(100), nullable = False, unique = True)
        password = db.Column(db.String(255), nullable = False, unique = True)
        user_type = db.Column(db.String(20),default = 'author')

        image = db.Column(db.String(100), nullable = True)
        biography = db.Column(db.String(100), nullable = False)
        created_at = db.Column(db.DateTime, default = datetime.now())   # This is a time stamp
        updated_at = db.Column(db.DateTime, onupdate = datetime.now())  # This is a time stamp
        
        # Defining all the attributes (Creating a constractor) This is because  incase you create any new user, all these fields will be required
        def __init__(self,first_name,last_name, author_contact,email_addresss,user_type, password, image, biography ):
         
        #  self.id = id
         self.first_name = first_name
         self.last_name = last_name
         self.author_contact = author_contact
         self.email_addresss = email_addresss
         self.user_type=user_type
         self.password = password
         self.image = image
         self.biography = biography
        #  self.created_at = created_at
        #  self.updated_at = updated_at


        def get_full_name(self):
             return f"{self.last_name} {self.first_name}"
              


         
              
        