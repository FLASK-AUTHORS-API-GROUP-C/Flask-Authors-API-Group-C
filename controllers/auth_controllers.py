
from flask import Blueprint,request,jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token



#auth Blueprint
auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth')


#User registration

@auth.route('/register', methods = ['POST'])
def register_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    author_contact = data.get('author_contact')
    email_address = data.get('email_address')
    password = data.get('password')
    image = data.get('image')
    biography = data.get('biography')  if type == 'author' else ''
    created_at = data.get('created_at')
    updated_at= data.get('updated_at')


    if not first_name or not last_name or not author_contact or not email_address:
        return jsonify({"error: All fileds are required" }),HTTP_400_BAD_REQUEST
    
    if type == 'author' and not biography:
        return jsonify({'error': "Enter your author biography"}),HTTP_400_BAD_REQUEST
    
    if len(password) < 8:
        return jsonify({'error': "Password is too short"}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email_address):
        return jsonify({"error":"Email is invalid"}),HTTP_400_BAD_REQUEST
    
    if  Author.query.filter_by(email_address=email_address).first() is not None:
          return jsonify({"error":"Email address in use"}),HTTP_409_CONFLICT
    
    if Author.query.filter_by(author_contact=author_contact).first() is not None:
          return jsonify({"error":"Phone number already in use"}),HTTP_409_CONFLICT
    
    try:
         hashed_password  = bcrypt.generate_password_hash('hunter2')# Hashing password


        #Creating the user
         new_author = Author(first_name=first_name,last_name=last_name,password=hashed_password,email_addresss=email_address,author_contact=author_contact,biography=biography,updated_at=updated_at,created_at=created_at,image=image)
         db.session.add(new_author)
         db.session.commit()

         # Author name
         authorname = new_author.get_full_name()


         return jsonify({
              'message': authorname + 'has been successfully created as a' + new_author.user_type,
              'author':{
                   
                   'first_name':new_author.first_name,
                   'last_name':new_author.last_name,
                   'author_contact':new_author.author_contact,
                   'email_address':new_author.email_addresss,
                   'password':new_author.password,
                   'biography':new_author.biography,
                   'id':new_author.id
                
                 

              }
         }),HTTP_201_CREATED
    except Exception as e:
         db.session.rollback()
         return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

    
    
    #User login
@auth.post('/login')  # This is implemented in the auth blueprint
def login():
    email_address = request.json.get('email_address')
    password = request.json.get('password')

    try:
        if not password or not email_address:
            return jsonify({'Message': 'Email and password are required'}), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email_address=email_address).first()

        if author:
            # Corrected variable name and comparison
            is_correct_password = bcrypt.check_password_hash(author.password, password)
            
            if is_correct_password:
                access_token = create_access_token(identity=author.id)

                return jsonify({
                    'user': {
                        'id': author.id,
                        'username': author.get_full_name(),  # Corrected method call
                        'email': author.email_address,  # Fixed typo
                        'access_token': access_token
                    }
                }), HTTP_200_OK

            else:
                return jsonify({'message': 'Invalid password'}), HTTP_400_BAD_REQUEST

        else:
            return jsonify({'Message': 'Invalid email address'}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR


