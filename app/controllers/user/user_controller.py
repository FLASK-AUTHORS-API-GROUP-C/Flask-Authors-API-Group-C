
from flask import Blueprint,request,jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_200_OK,HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND
import validators
from app.models.author_model import Author
from app.extensions import db,bcrypt
#from app.controllers.user.user_controller import users

from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,create_refresh_token



#users Blueprint defining the blueprint
users = Blueprint('users',__name__,url_prefix='/api/v1/users') # defining the prefix for api,version 1 and the table


# getting all users from the database
@users.get('/')
def getAllUsers():
    # email = request.json.get('email')
    # password = request.json.get('password')

    try:

        all_users = Author.query.all()
        users_data = []
        for user in all_users:
            user_info = {
                'id' : user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username' : user.get_full_name(),
                'email' : user.contact,
                'created_at': user.created_at


            }
            users_data.append(user_info)

            return jsonify({
                'message' : "All users retrieved succesfully",
                'total_user' : len(users),
                'users' : users_data

            }),HTTP_200_OK


        return jsonify(all_users)
    
    

    except Exception as e:
        return jsonify ({
            'error': str(e)

        }),HTTP_500_INTERNAL_SERVER_ERROR

# Getting all authors
@users.get('/authors')
def GetAllAuthors():

    try:
        all_authors = Author.query.filter_by().all()
        authors_data = []
        
        for author in all_authors:
            author_info = {
                'id' : author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'username' : author.get_full_name(),
                'email' : author.contact,
                'biography' : author.biography,
                'created_at': author.created_at,
                'companies': [],
                'book': []

            }

            if hasattr(author,'book'):
                 
                    author_info['book'] = [ { 'id':book.id,'title':book.title,'price':book.price,'genre':book.id,'description':book.description,'publication':book.publication_date,'image':book.image,'created_at':book.created_at} for book in author.book ]
                
            if hasattr(author,'companies'):
                    
                        author_info['companies'] = [ { 'id':company.id,'name':company.name,'origin':company.origin,'description':company.description,'image':company.image,'created_at':company.created_at}for company in author.company]
    




            authors_data.append(author_info)

            return jsonify({
                'message' : "All users retrieved succesfully",
                'total' : len(authors_data),
                'authors' : authors_data

            }),HTTP_200_OK


        return jsonify(all_authors)                                   
    
    

    except Exception as e:
        return jsonify ({
            'error': str(e)

        }),HTTP_500_INTERNAL_SERVER_ERROR



# Getting a user by id

@users.get('/user/<int:id>')
@jwt_required()
def GetUser(id):

    try:
        user = Author.query.filter_by(id=id).first()


        books = []
        companies = []

        
        if hasattr(user,'books'):
                 
        
            books = [ { 'id': book.id, 'title': book.title, 'price': book.price, 'genre': book.id, 'description': book.description, 'publication': book.publication_date, 'image': book.image } for book in user.book ]

                
        if hasattr(user,'companies'):
                    
    
            companies = [ { 
    'id': company.id,
    'name': company.name,
    'origin': company.origin,
    'description': company.description,
    'image': company.image 
} for company in user.company ]


        return jsonify({
             "message": "user details restricted succesfully",

             "user":{
                  'id' : user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username' : user.get_full_name(),
                'email' : user.contact,
                'biography' : user.biography,
                'created_at': user.created_at,
                'companies': companies,
                'books': books

             }
                 
            })

    except Exception as e:
        return jsonify ({
            'error': str(e)

        }),HTTP_500_INTERNAL_SERVER_ERROR


#updating user details

@users.route('/user/<int:id>',methods = ['PUT','PATCH'])
@jwt_required()
def UpdateUserDetails(id):

    try:
         current_user = get_jwt_identity()
         logged_in_user = Author.query.filter_by(id=current_user).first()

         user = Author.query.filter_by(id=id).first()
         if not user:
              return jsonify({"error":"User not found"}), HTTP_404_NOT_FOUND
         elif logged_in_user.user_type!= 'admin' and user.id != current_user:
              return jsonify({"error": "You are not authorised to update the user details"})
         else:
              first_name = request.get_json().get('first_name',user.first_name)
              last_name = request.get_json().get('last_name',user.last_name)
              biography = request.get_json().get('biography',user.biography)
              contact = request.get_json().get('contact',user.contact)
              email= request.get_json().get('email',user.email)
              password= request.get_json().get('password',user.password)


              if "password" in request.json:
                   hashed_password = bcrypt.generate_password_hash(request.json.get('password'))
                   user.password = hashed_password


                   user.first_name = first_name
                   user.last_name = last_name
                   user.email = email
                   user.contact = contact
                   user.biography = biography

                   db.session.commit()

                   user_name = user.get_full_name()

                   return jsonify({
                        'message':user_name + "User's details have been successfully updated",
                        'user': {
                              'id' : user.id,
                              'first_name': user.first_name,
                              'last_name': user.last_name,
                              'contact': user.contact,
                              'email' : user.contact,
                              'biography' : user.biography,
                              'updated_at': user.updated_at,


                        }

                   })


    
   
         


    except Exception as e:
        return jsonify ({
            'error': str(e)

        }),HTTP_500_INTERNAL_SERVER_ERROR







