from flask import Blueprint,request,jsonify
from app.statuscode import HTTP_400_BAD_REQUEST,HTTP_409_NOT_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token


# auth blueprint
auth = Blueprint('auth', __name__,url_prefix='/api/v1/auth')

# user registration

@auth.route("/register,methods=['POST']")
def register_author():

    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email   = data.get('email')
    contact = data.get('contact')
    password= data.get('password')
    biography = data.get('biography', '')if type == "author" else ''
    author_type =data.get('author_type') if author_type in data else "author"


    # validations for the incoming requests
    if not first_name or not last_name or not email or not password:
        return jsonify({"error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    if type == 'author' and not biography:
        return jsonify({"error":"Enter the author's biography."}),HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({"error":"The password is too short."}),HTTP_400_BAD_REQUEST
    

    if not validators.email:
        return jsonify({"error":"Email is not valid."}),HTTP_400_BAD_REQUEST
    
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"Email address already in use."}),HTTP_409_NOT_CONFLICT
    
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Phone number already in use."}),HTTP_409_NOT_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash('password') # hashing the password

        # Creating an author
        new_author=Author(first_name=first_name,last_name=last_name,password=hashed_password,email=email,
                          contact=contact,biography=biography,author_type=author_type)
        db.session.add(Author)
        db.session.commit()

        # author name
        author_name =new_author.get_full_name()

        return jsonify({
            "message":author_name + "has been successfully created as a "+ new_author.author_type, 
            "user":{
                "first_name":new_author.first_name,
                "last_name":new_author.last_name,
                "email":new_author.email,
                "contact":new_author.contact,
                "password":new_author.password,
                "biography":new_author.biography,
                }
                
            }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    



    # user login
@auth.post('/login')  
def login():
    try:
        # Retrieve email and password from request JSON
        email = request.json.get('email')
        password = request.json.get('password')

        # Validating the input fields
        if not email or not password:
            return jsonify({'message': "Email and password are required."}), HTTP_400_BAD_REQUEST

        # Fetch user from the database
        user = Author.query.filter_by(email=email).first()  # Fix: Use `.first()` to get a single user object

        # Check if user exists
        if not user:
            return jsonify({"message": "Invalid email address."}), HTTP_401_UNAUTHORIZED

        # Verify the password (assuming passwords are hashed)
        if not password(user.password, password):
            return jsonify({"message": "Invalid password."}), HTTP_401_UNAUTHORIZED

        # Generate JWT token (if using Flask-JWT-Extended)
        access_token = create_access_token(identity=user.id)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token
        }),HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR