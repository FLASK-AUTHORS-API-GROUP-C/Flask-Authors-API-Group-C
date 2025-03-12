class Config: #The connection string shd be in the config file
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/author_db"
    JWT_SECRET_KEY = "authors"