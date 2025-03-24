from flask import Blueprint,request,jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_NOT_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.book_model import Book
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,jwt_required

# books blue print
books = Blueprint('book', __name__,url_prefix='/api/v1/books')

# creating a new book
@books.route("/create ",methods =["POST"])

# for security purposes we use a jwt decorator
@jwt_required()
def createNewBook():

#storing the json data that is coming from the request body.
    data = request.get_json()
    book_id = data.get('book_id')
    title = data.get('title')
    price = data.get('price')
    image = data.get('image') 
    publication_date = data.get('publication_date')
    description =data.get('description')
    no_of_pages = data.get('no_of_pages')
    isbn = data.get('isbn')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')
    author_id = data.get('author_id')
    company_id = data.get('company_id')
    company = data.get('company')
    author = data.get('author')

# validations for the incoming requests
    if not title or not price or not description or not no_of_pages or not publication_date or not isbn or not company_id:
        return jsonify({"error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    # checking if the incoming book title is similar with the existing one.
    if Book.query.filter_by(title = title, author_id = author_id).first() is not None:
        return jsonify({"error":"Book with this title  and author_id are already exists."}),HTTP_409_NOT_CONFLICT
    
    # checking if the incoming book isbn is similar with the existing one.
    if Book.query.filter_by(isbn = isbn).first() is not None:
        return jsonify({"error":"Book isbn is already in use."}),HTTP_409_NOT_CONFLICT
    
    try:
    
     # Creating a new book
        new_book=Book(
            book_id = book_id,
            title = title,
            price = price,
            publication_date = publication_date,
            description =description,
            no_of_pages = no_of_pages,

            )
        db.session.add(new_book)
        db.session.commit()

        # book name
        book_name = new_book.get_title()

        return jsonify({
            "message":title + "has been successfully created ", 
            "book":{
                "title":new_book.title,
                "book_id":new_book.book_id,
                "price":new_book.price,
                "description":new_book.description,
                "no_of_pages":new_book.no_of_pages,
                "publication_date":new_book.publication_date,
            # we add a new key for a company
                 "company":{
                       "name":new_book.company.name,
                        "id":new_book.company.id,
                        "email":new_book.company.email,
                        "contact":new_book.company.contact,
                        "origin":new_book.company.origin,
                        "description":new_book.company.description,
                 },
                 # we add a new key called author
                 "author":{
                        "first_name":new_book.author.first_name,
                        "last_name":new_book.author.last_name,
                        "email":new_book.author.email,
                        "contact":new_book.author.contact,
                        "password":new_book.author.password,
                        "bio":new_book.author.bio
                 }
                 
                }
                
            }),HTTP_201_CREATED
    except Exception as e:
            db.session.rollback()
            return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR







