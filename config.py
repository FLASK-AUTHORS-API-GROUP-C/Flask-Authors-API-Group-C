# Create a class called config
# This id the connection string
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/authors_db'

    JWT_SECRET_KEY= "author"




