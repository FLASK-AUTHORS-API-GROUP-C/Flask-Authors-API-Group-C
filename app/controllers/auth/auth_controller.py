from flask import Blueprint,request,jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_NOT_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity


# auth blueprint
auth = Blueprint('auth', __name__,url_prefix='/api/v1/auth')

# author registration

@auth.route("/register",methods=['POST'])
def register_author():

    data = request.json
    author_id =data.get('author_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email   = data.get('email')
    contact = data.get('contact')
    password= data.get('password')
    bio = data.get('bio', '')


   
    # validations for the incoming requests
    if not first_name or not last_name or not email :
        return jsonify({"error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    if not password:
        return jsonify({"error": "Password is required."}),HTTP_400_BAD_REQUEST
    print("Received Password:", password)
   
    # ensuring the user enters the author's biography
    if not bio:
        return jsonify({"error":"Enter the author's biography."}),HTTP_400_BAD_REQUEST
    
    # ensuring that the password is not too short
    if len(password) < 8:
        return jsonify({"error":"The password is too short."}),HTTP_400_BAD_REQUEST
    
    # ensuring validity of the email.
    if not validators.email(email):
        return jsonify({"error":"Email is not valid."}),HTTP_400_BAD_REQUEST
    
    # checking if the incoming email is similar with the existing one.
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"Email address already in use."}),HTTP_409_NOT_CONFLICT
    
    # checkin if the incoming contact is already in use.
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Phone number already in use."}),HTTP_409_NOT_CONFLICT
    


    #we hash the password to ensure encryption.(we dont have unauthorised access.)
    # we use bcrypt for hashing.
    # Bcrypt is a flask extension that provides bcrypt hashing utilies for an application.
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') # hashing the password
    
      
        # Creating an author
        new_author=Author(
            author_id =author_id,
            first_name = first_name,
            last_name = last_name,
            password = hashed_password,
            email = email,
            contact = contact,
            bio = bio
            )
        db.session.add(new_author)
        db.session.commit()

        # author name
        author_name =new_author.get_full_name()

        return jsonify({
            "message":author_name + "has been successfully created ", 
            "author":{
                "first_name":new_author.first_name,
                "last_name":new_author.last_name,
                "email":new_author.email,
                "contact":new_author.contact,
                "password":new_author.password,
                "bio":new_author.bio,
                "author_id":new_author.author_id
                }
                
            }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    


# author login
@auth.route('/login',methods=['POST']) 
def login():
 # Retrieve email and password from request JSON
    email = request.json.get("email")
    password = request.json.get("password")

    try:
       
       # Validating the input fields
        if not email or not password:
            return jsonify({'message': "Email and password are required."}), HTTP_400_BAD_REQUEST

        # Fetch user from the database
        author = Author.query.filter_by(email=email).first()  # Fix: Use `.first()` to get a single user object

        # Check if user exists
        if author:
            is_correct_password = bcrypt.check_password_hash(author.password,password)

            if is_correct_password:
                # Generate JWT token (if using Flask-JWT-Extended)
                access_token = create_access_token(identity=author.author_id)
                refresh_token = create_refresh_token(identity=author.author_id)
                return jsonify({
                    "author":{
                        "author_id":author.author_id,
                        "name":author.get_full_name(),
                        "email":author.email,
                        "access_token":access_token,
                        "refresh_token":refresh_token
                    },
                    "message" :"You have successsfully logged into your account."
                
                }), HTTP_200_OK
            else:
                return jsonify({"message":"Invalid  password"}),HTTP_401_UNAUTHORIZED


          
        else:
            return jsonify({"message": "Invalid email address."}), HTTP_401_UNAUTHORIZED
        

        
        

# for catching errors that arise during the  process of testing this end point.
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    

@auth.route("/token/refresh",methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = str(get_jwt_identity())
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token" : access_token})