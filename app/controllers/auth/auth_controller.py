from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_NOT_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN
import validators
from app.models.author_model import Author
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity

# auth blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# author registration
@auth.route("/register", methods=['POST'])
def register_author():
    data = request.json
    author_id = data.get('author_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    contact = data.get('contact')
    password = data.get('password')
    bio = data.get('bio', '')

    # validations for the incoming requests
    if not first_name or not last_name or not email:
        return jsonify({"error": "All fields are required."}), HTTP_400_BAD_REQUEST
    
    if not password:
        return jsonify({"error": "Password is required."}), HTTP_400_BAD_REQUEST
    print("Received Password:", password)
    
    # ensuring the user enters the author's biography
    if not bio:
        return jsonify({"error": "Enter the author's biography."}), HTTP_400_BAD_REQUEST
    
    # ensuring that the password is not too short
    if len(password) < 8:
        return jsonify({"error": "The password is too short."}), HTTP_400_BAD_REQUEST
    
    # ensuring validity of the email.
    if not validators.email(email):
        return jsonify({"error": "Email is not valid."}), HTTP_400_BAD_REQUEST
    
    # checking if the incoming email is similar with the existing one.
    if Author.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email address already in use."}), HTTP_409_NOT_CONFLICT
    
    # check if the incoming contact is already in use.
    if Author.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error": "Phone number already in use."}), HTTP_409_NOT_CONFLICT

    # we hash the password to ensure encryption.
    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # hashing the password
    
        # Creating an author
        new_author = Author(
            author_id=author_id,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            bio=bio
        )
        db.session.add(new_author)
        db.session.commit()

        # author name
        author_name = new_author.get_full_name()

        return jsonify({
            "message": author_name + " has been successfully created ",
            "author": {
                "first_name": new_author.first_name,
                "last_name": new_author.last_name,
                "email": new_author.email,
                "contact": new_author.contact,
                "password": new_author.password,
                "bio": new_author.bio,
                "author_id": new_author.author_id
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# author login
@auth.route('/login', methods=['POST']) 
def login():
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
            is_correct_password = bcrypt.check_password_hash(author.password, password)

            if is_correct_password:
                # Generate JWT token (if using Flask-JWT-Extended)
                access_token = create_access_token(identity=str(author.author_id))
                refresh_token = create_refresh_token(identity=str(author.author_id))

                return jsonify({
                    "author": {
                        "author_id": author.author_id,
                        "name": author.get_full_name(),
                        "email": author.email,
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                    "message": "You have successfully logged into your account."
                }), HTTP_200_OK
            else:
                return jsonify({"message": "Invalid password"}), HTTP_401_UNAUTHORIZED
        else:
            return jsonify({"message": "Invalid email address."}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


@auth.route("/token/refresh", methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = str(get_jwt_identity())
    access_token = create_access_token(identity=identity)
    return jsonify({"access_token": access_token})


# Getting all authors from the database.
@auth.get('/authors')
@jwt_required()
def get_all_authors():
    try:
        all_authors = Author.query.all()

        author_data = []

        for author in all_authors:
            author_info = {
                "author_id": author.author_id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "email": author.email,
                "contact": author.contact,
                "bio": author.bio,
                "created_at": author.created_at,
                "companies": [],
                "books": []
            }

            # Checking if the attribute has the data we want to access.
            if hasattr(author, 'books'):
                author_info['books'] = [{
                    "id": book.book_id,
                    "description": book.description,
                    "publication": book.publication_date,
                    "title": book.title,
                    "price": book.price,
                    "image": book.image,
                    "no_of_pages": book.no_of_pages,
                    "created_at": book.created_at
                } for book in author.books]
            if hasattr(author, 'companies'):
                author_info['companies'] = [{
                    'company_id': company.company_id,
                    'name': company.name,
                    'origin': company.origin,
                    'email': company.email
                } for company in author.companies]

            author_data.append(author_info)

        return jsonify({
            "message": "All users retrieved successfully",
            "total_authors": len(author_data),
            "authors": author_data
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Get author by id.
@auth.get('/authors/<int:id>')
@jwt_required()
def get_author(author_id):
    try:
        author = Author.query.filter_by(author_id=author_id).first()

        books = []
        companies = []

        if not author:
            return jsonify({"error": "Author not found."}), HTTP_404_NOT_FOUND

        if hasattr(author, 'books'):
            books = [{
                "id": book.book_id,
                "description": book.description,
                "publication": book.publication_date,
                "title": book.title,
                "price": book.price,
                "image": book.image,
                "no_of_pages": book.no_of_pages
                
            } for book in author.books]
        
        if hasattr(author, 'companies'):
            companies = [{
                'company_id': company.company_id,
                'name': company.name,
                'origin': company.origin,
                'email': company.email
            } for company in author.companies]

        return jsonify({
            "author": author.author_id,
            "first_name": author.first_name,
            "last_name": author.last_name,
            "email": author.email,
            "contact": author.contact,
            "bio": author.bio,
            "created_at": author.created_at,
            "companies": companies,
            "books": books
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Updating the author details
@auth.route('/edit/<int:author_id>', methods=['GET'])
@jwt_required()  # protecting the route with authentications
def update_author_details(author_id):
    try:
        
        author = Author.query.filter_by(author_id=author_id).first()

        if not author:
            return jsonify({"error": "Author not found."}), HTTP_404_NOT_FOUND
        
        

        else:
        

            author_name = author.get_full_name()

            return jsonify({
                'message': author_name + " has been successfully updated",
                "author": author.author_id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "email": author.email,
                "contact": author.contact,
                "bio": author.bio,
                "created_at": author.created_at,
            })

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

        
# Resetting the password
@auth.route('/reset-password', methods=['POST'])
def reset_password():
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        new_password = data.get('new_password')

        if not first_name or not last_name or not new_password:
            return jsonify({"error": "First_name , last_name and new password are required."}), HTTP_400_BAD_REQUEST

        try:
            author = Author.query.filter_by(first_name = first_name , last_name = last_name).first()

            if not author:
                return jsonify({"error": "Author not found."}), HTTP_404_NOT_FOUND

            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            author.password = hashed_password

            db.session.commit()

            return jsonify({"message": "Password reset successfully"}), HTTP_200_OK

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


    

# deleting the author
@auth.route('/delete/<int:author_id>',methods=['DELETE'])
@jwt_required()
def delete_author(author_id):
    author = Author.query.get(author_id)
    if not author:
        return jsonify({"message": "Author not found."}), HTTP_404_NOT_FOUND
    try:
        #delete associated companies if they exist
        if hasattr(author, 'companies') and author.companies:
            for company in author.companies:
                db.session.delete(company)
        # delete associated books if they exist
        if hasattr(author, 'books') and author.books:
            for book in author.books:
                db.session.delete(book)

        # Delete the author
        db.session.delete(author)
        db.session.commit()
        return jsonify({"message": "Author deleted successfully"}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
