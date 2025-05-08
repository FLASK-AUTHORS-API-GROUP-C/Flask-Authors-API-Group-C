from flask import Blueprint,request,jsonify
from app.status_code import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED
from flask import Flask
import validators
from app.models.book_model import Book
from app.extensions import db,bcrypt
from flask_jwt_extended import JWTManager, jwt_required,get_jwt_identity



 #book blueprint
book = Blueprint('book', __name__,url_prefix = '/api/v1/book') #it's used to define routes related to books.


#Creating  new  books
@book.route('/create',methods=['POST'])
@jwt_required()

def create_newbook():

   # storing request data
    data = request.get_json()
    title = data.get('title')
    pages = data.get('pages')
    price = data.get('price')
    unit_price = data.get('unit_price')
    description = data.get('description')
    genre = data.get('genre')
    isbn = data.get('isbn')
    publication_date = data.get('publication_date')
    image = data.get('image')
    company_id = data.get('company_id')
    author_id = get_jwt_identity()



#validating the incoming request
    if not title or not isbn  or not description or not price or not price_unit or not genre or not publication_date or not company_id:
            return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST
#This is used to convert Python dictionaries into JSON format
    
    if Book.query.filter_by(title=title,author_id=author_id).first() is not None:      
          return jsonify({"error": "Book with this title and author id already exists"}), HTTP_400_BAD_REQUEST


    if Book.query.filter_by(isbn=isbn).first() is not None:      
          return jsonify({"error": "Book with this title and author id already exists"}), HTTP_400_BAD_REQUEST

    try:
          
          #creating a new book

          new_book = Book(title=title,
                          pages=pages,
                          image=image,
                          isbn=isbn,
                          genre=genre,
                          unit_price=unit_price,
                          publication_date=publication_date,
                          company_id=company_id,
                          author_id=author_id)
                        
          db.session.add(new_book)  #This is the database extension for SQLAlchemy, used to interact with the database.
          db.session.commit()
           
          return jsonify({
    'message': title + " has been created successfully",
    'book': {
        'id': new_book.id,
        'title': new_book.title,
        'price': new_book.price,
        'unit_price': new_book.unit_price,
        'description': new_book.description,
        'pages': new_book.pages,
        'isbn': new_book.isbn,
        'genre': new_book.genre,
        'publication_date': new_book.publication_date,
        'company': {
            'company_id': new_book.company.id,
            'name': new_book.company.name,
            'origin': new_book.company.origin,
            'description': new_book.company.description,
        },
        
        'author':{
              "first_name":new_book.author.first_name,
              "last_name":new_book.author.last_name,
              "email":new_book.author.email,
              "contact":new_book.author.contact,
              "type":new_book.author.user_type,
        },

        'image': new_book.image,
    }
}), HTTP_201_CREATED


    except Exception as e:
          db.session.rollback()
          return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

       
         