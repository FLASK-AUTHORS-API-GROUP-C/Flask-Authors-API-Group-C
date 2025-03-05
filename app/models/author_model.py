from app.extensions import db
from datetime import datetime


class Author(db.Model):
        __tablename__ = "authors"
        id=db.Column(db.Integer,primary_key=True, nullable=False)
        first_name =db.Column(db.String(100) ,nullable = False)
        last_name =db.Column(db.String(100),nullable =False)
        email =db.Column(db.String(100),nullable = False,unique =True)
        contact =db.Column(db.Integer,nullable = False,unique =True)
        password =db.Column(db.Text,nullable = False)
        image =db.Column(db.String(255),nullable = True)
        bio =db.Column(db.Text,nullable = False,unique =True)
        author_type=db.Column(db.String,nullable = False,unique =False)
        created_at =db.Column(db.DateTime,default = datetime.now())
        updated_at = db.Column(db.DateTime,onupdate =datetime.now() )

        def __init__(self,id,first_name,last_name,email,contact,password,image,bio): 
                self.id =id
                self.first_name =first_name
                self.last_name =last_name
                self.email =email
                self.contact =contact
                self.passsword =password
                self.image = image
                self.bio =bio
                 
        def get_full_name(self): 
                return f"{self.first_name} {self.last_name}"