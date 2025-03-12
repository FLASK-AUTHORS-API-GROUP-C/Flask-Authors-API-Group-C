from app.extensions import db
from datetime import datetime


class Author(db.Model):
        __tablename__ = "authors"
        author_id=db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
        first_name =db.Column(db.String(100) ,nullable = False)
        last_name =db.Column(db.String(100),nullable =False)
        email =db.Column(db.String(100),nullable = False,unique =True)
        contact =db.Column(db.Integer,nullable = False,unique =True)
        password =db.Column(db.String(255), nullable = False,unique=True)
        bio =db.Column(db.Text,nullable = False,unique =True)
        created_at =db.Column(db.DateTime,default = datetime.now)
        updated_at = db.Column(db.DateTime,onupdate =datetime.now)

        # company_id = db.Column(db.Integer, db.ForeignKey("company_id"),nullable=True)
        # book_id =db.Column(db.Integer ,primary_key=True)

        # books = db.relationship("Book" , backref ="author")
        

        def __init__(self,first_name,last_name,email,contact,password,bio):
                super(Author,self).__init__()
                self.first_name =first_name
                self.last_name =last_name
                self.email =email
                self.contact =contact
                self.passsword =password
                self.bio = bio
                 
        def get_full_name(self): 
                return f"{self.first_name} {self.last_name}"
