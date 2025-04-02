from flask import Blueprint,request,jsonify  # The bluerprint  is for verifying the endpionts, request is to ensure we get the responses from jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_403_FORBBIDEN
import validators  # This is for validating the emails
from app.models.author_model import Author # This is to enable us to access the Author model attributes, And to make queries to the database checking whether somethings appear twice.
from app.models.company_model import Company
from app.models.book_model import Book
from app.extensions import db,bcrypt  # This is to ensure that we roll back incase of any mistakes. (we undo any steps) 
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
# from email_validator import validate_email ,EmailNotValidError




 
#auth Blueprint
auth = Blueprint('auth',__name__,url_prefix='/api/v1/auth') # 'auth' is the name we are going to use for grouping of the blueprints


#Author registration
#
@auth.route('/register',methods = ['POST'])  # The decorator must piont at the name of the object Blueprint  thats why e use 'auth'
#We use registor as the end ponit and ['POST'] as the method for creating
# So from flask we import request 
#Te route is used to bind the 


# Define the function
def register_user():
    # We ned to use 'request' response cycle such that a user can make a request and it return the response.
    # So we work with a variable tha is going to store the incoming requests from the user and returns a particular response.
    data = request.json
    # We now enter the data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    author_contact = data.get('author_contact')
    email_addresss = data.get('email_addresss')
    user_type= data.get('user_type')
    password = data.get('password')
    image = data.get('image')
    biography = data.get('biography')  if type == 'author' else ''
   
# We need to ensure that  we are not having redadunt data because we are wworking with data bases.
# First we e nsure that all the required attributes on our model are being submitted within our request.
    if not first_name or not last_name or not author_contact or not email_addresss  or not password:
        return jsonify({"error": "All fields are required" }),HTTP_400_BAD_REQUEST
    
    if type == 'author' and not biography:
        return jsonify({'error': "Enter your author biography"}),HTTP_400_BAD_REQUEST
    
    if len(password) < 8: # Password not be less tha 8 characters
        return jsonify({'error': "Password is too short"}),HTTP_400_BAD_REQUEST
    
     #We work with the validators to ensure that the email address is te valid one from the request. 
     #This is because this library has the email function that we can use to pas in a particular email that we want to validate. 
     #So we install validators and import the validors    
    if not validators.email(email_addresss):
        return jsonify({"error":"Email is invalid"}),HTTP_400_BAD_REQUEST
    
    # We have to make a query to the database to  that there is no such request already in the database.
    # #Therefore we have to import it from our package as the author model which is the Author. 
    if  Author.query.filter_by(email_addresss=email_addresss).first() is not None: # This checks whether the email address was already in use
          return jsonify({"error":"Email address already in use"}),HTTP_409_CONFLICT # This is used whenever there is a violation or something that already exists
    
    if Author.query.filter_by(author_contact=author_contact).first() is not None:   # This checks whether the contact was already in use
          return jsonify({"error":"Phone number already in use"}),HTTP_409_CONFLICT  # This is used whenever there is a violation or something that already exists
    
    #  While Creating a new user, we work with the hashing
    # Hashing is used to encript(No user can understand)
    # We hash the paasswords inorder to encript security

# We now work with the  logic that stores a new user to the database.

    try:
         # We have to work with a third party library that will help hash our paswords which is bcrypt.
         # Therefore we install Bcrypt. 
         # And import it.
         hashed_password  = bcrypt.generate_password_hash(password)# Hashing password


        #Creating the  new instance for our  Author
         new_author = Author( first_name=first_name,last_name=last_name,password=hashed_password,email_addresss=email_addresss,author_contact=author_contact,user_type=user_type, biography=biography,image=image)
         
# Inorder to store the new user object, we have to add that object to   the session and the commit 

         db.session.add(new_author) # Add our new user vairable
         db.session.commit()
         db.session.refresh(new_author)
         db.session.rollback() # Then commit



         # Define a variable that keeps track of the author name
         author_name = new_author.get_full_name()

# Then return a message that says the new user has been created.
         return jsonify({
              'message': author_name + 'has been successfully created as an author',
              #Return user object to the response. This is inform of a dictionary
              'author':{
                   
                   'first_name':new_author.first_name,
                   'last_name':new_author.last_name,
                   'author_contact':new_author.author_contact,
                   'email_addresss':new_author.email_addresss,
                   'password':new_author.password,
                   'biography':new_author.biography,
                   'id':new_author.id
                
                 

              }
         }),HTTP_201_CREATED

         # We now have to work with error handeling while creating a new user.
         # Ths is to ensure that for any mistakes arise in the during the process of creating a user  we roll back to the database
    except Exception as e:
         db.session.rollback() #Return back to the database.
         return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR  # This is the response of the eror that we are having at hand.
    

    



    
    #User login
@auth.post('/login')  # This is implemented in the auth blueprint
def login():
    email_addresss = request.json.get('email_addresss')
    password = request.json.get('password')

    try:
        if not password or not email_addresss:
            return jsonify({'Message': 'Email and password are required'}), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email_addresss=email_addresss).first()

        if author:
            # Corrected variable name and comparison
            is_correct_password = bcrypt.check_password_hash(author.password, password)
            refresh_token = create_refresh_token(identity=author.id)
            

            if is_correct_password:
                access_token = create_access_token(identity=author.id)
                refresh_token = create_refresh_token(identity=author.id)

                return jsonify({
                    'user': {
                        'id': author.id,
                        'username': author.get_full_name(),  # Corrected method call
                        'email': author.email_addresss,  # Fixed typo
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    },
                    'message': "Login successfully"
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
    


# Refreshing Token
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = str(get_jwt_identity())
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token})
    


# Get all  aothors from the database
@auth.get('/authors')
def getAllAuthors():

    try:
        all_authors = Author.query.filter_by(user_type = 'author').all()

        authors_data = []
        for author in all_authors:
            author_info = {
                'id':author.id,
                'first_name':author.first_name,
                'last_name':author.last_name,
                'user_name':author.get_full_name(),
                'email_addresss':author.email_addresss,
                'author_contact':author.author_contact,
                'biography': author.biography,
                'created_at':author.created_at,
                # 'companies':[],
                'books':[]
               

            }

            if hasattr(author, 'books'):
                author_info['books'] = [{'id': book.id, 'title': book.title, 'price':book.price, 'genre': book.id, 'price_unit': book.price_unit, 'description': book.description, 'publication': book.publication_date,  'image': book.image, 'created_at': book.created_at} for book in author.books]



            # if hasattr(author, 'companies'):
            #     author_info['companies'] = [{'id': company.id, 'name':company.name, 'origin': company.origin} for company in author.company]  

            # Access the authors list

            authors_data.append(author_info)

        # Ensure that the variable is serialised. This means us having the ability to access the value that is converted to json easily.
        return jsonify({
            'message':'All authors retrieved successfuly',
            'total': len(authors_data),
            'authors': authors_data  #This will return authors data list

        }),HTTP_200_OK
    



    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR





# Deleting author

@auth.route('/delete/<int:id>', methods = ['DELETE'])
@jwt_required()
def deleteAuthor(id):
     try:
         current_author = get_jwt_identity()
         loggedInAuthor = Author.query.filter_by(id=current_author).first()

         # Get author by id
         author = Author.query.filter_by(id=id).first()


         if not author: 
             return jsonify({'error': 'Author not found'}),HTTP_404_NOT_FOUND
         elif loggedInAuthor.author_type!= 'admin':
             return jsonify({'error': 'You are not authorised to delete this author'}),HTTP_403_FORBBIDEN
         
         
         

         

     except Exception as e:
         return jsonify({
             'error': 'Athour deleted successflly'
         }),HTTP_404_NOT_FOUND


