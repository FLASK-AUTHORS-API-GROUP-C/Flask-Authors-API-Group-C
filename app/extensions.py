from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask import jsonify


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
