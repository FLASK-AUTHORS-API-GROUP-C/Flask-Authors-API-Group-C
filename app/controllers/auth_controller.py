
from flask import Blueprint,request,jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_200_OK,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,create_refresh_token



#auth Blueprint defining the blueprint
auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth') # defining the prefix for api,version 1 and the table


#User registration

@auth.route('/register', methods = ['POST']) #Post is used when creating and registering users and json representaion format []
def register_author(): # registering the user
    data = request.json # variable of object storing data
    first_name = data.get('first_name') #accessing variables from the table
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    biography = data.get('biography', '')  
    created_at = data.get('created_at')
    updated_at= data.get('updated_at')


#Request response cycle 

    if not first_name or not last_name or not contact or not email: 
        return jsonify({"error": "All fileds are required" }),HTTP_400_BAD_REQUEST
    
    if not biography:
        return jsonify({'error': "Enter your author biography"}),HTTP_400_BAD_REQUEST
    
    #The length of the 
    if len(password) < 8: #Password should not be less than 8
        return jsonify({'error': "Password is too short"}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email): 
        return jsonify({"error":"Email is invalid"}),HTTP_400_BAD_REQUEST
    
    #key value pairs representing data to be accesed
    if  Author.query.filter_by(email=email).first() is not None: #Ensuring email and contact constrains 
          return jsonify({"error":"Email address in use"}),HTTP_409_CONFLICT #Accessing the model to check if the email is valid
    
    if Author.query.filter_by(contact=contact).first() is not None:
          return jsonify({"error":"Phone number already in use"}),HTTP_409_CONFLICT
    
    try:
         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')# Hashing password to encrypt password,to avoid unauthorised access


        #Creating the user
         new_author = Author(first_name=first_name,last_name=last_name,password=hashed_password,email=email,contact=contact,biography=biography)
         db.session.add(new_author)
         db.session.commit()

         # Author name
         authorname = new_author.get_full_name()


         return jsonify({
              'message': authorname + 'has been successfully created',
              'author':{
                   
                   'first_name':new_author.first_name,
                   'last_name':new_author.last_name,
                   'contact':new_author.contact,
                   'password':new_author.password,
                   'biography':new_author.biography,
                   'id':new_author.id
                
                 

              }
         }),HTTP_201_CREATED
    except Exception as e:
         db.session.rollback()
         return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

    
    
    #author login
@auth.post('/login') # This is implemented in the auth blueprint
def login_author():

    email = request.json.get('email')
    password = request.json.get('password')

    try:
        if not password or not email:
            return jsonify({'Message': 'Email and password are required'}), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email=email).first()

        if author:
            # Corrected variable name and comparison
            is_correct_password = bcrypt.check_password_hash(author.password, password)
            
            if is_correct_password:
                access_token = create_access_token(identity=author.id)
                refresh_token = create_refresh_token(identity=author.id)
                return jsonify({
                    'user': {
                        'id': author.id,
                        'username': author.get_full_name(),  # Corrected method call
                        'email': author.email_address, 
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                }), HTTP_200_OK

            else:
                return jsonify({'message': 'Invalid password'}), HTTP_400_BAD_REQUEST

        else:
            return jsonify({'message': 'Invalid email address'}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e) }), HTTP_500_INTERNAL_SERVER_ERROR



#We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)










