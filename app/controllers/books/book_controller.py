# Creating a new book

from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND
from app.models.book_model import Book
from app.extensions import db
from flask_jwt_extended import jwt_required,get_jwt_identity



 # Creating the book blueprint
book = Blueprint('books', __name__,url_prefix = '/api/v1/books')


#Creating books endpoints
@book.route('/create',methods=['POST'])
@jwt_required()

def create_newbook():

   # storing request data
    data = request.get_json()
    title = data.get('title')
    pages = data.get('pages')
    price = data.get('price')
    description = data.get('description')
    # genre = data.get('genre')
    isbn = data.get('isbn')
    publication_date = data.get('publication_date')
    image = data.get('image')
    company_id = data.get('company_id')
    author_id = data.get('author_id')



#validating the incoming request
    if not title  or not description or not price :
            return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    
    if Book.query.filter_by(title=title,author_id=author_id).first() is not None:      
          return jsonify({"error": "Book with this title and user id already exists"}), HTTP_400_BAD_REQUEST


    if Book.query.filter_by(isbn=isbn).first() is not None:      
          return jsonify({"error": "Book with this isbn already exists"}), HTTP_400_BAD_REQUEST

    try:
          
          #creating a new book

          new_book = Book(title=title,pages=pages,image=image,price=price,publication_date=publication_date,company_id=company_id)
                        
          db.session.add(new_book)
          db.session.commit()
           
          return jsonify({
    'message': title + " has been created successfully",
    'book': {
        'id': new_book.id,
        'title': new_book.title,
        'price': new_book.price,
        'description': new_book.description,
        'pages': new_book.pages,
        'genre': new_book.genre,
        'publication_date': new_book.publication_date,
        'company': {
            'id': new_book.company.id,
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
    




# Define the update book endpoint
@book.route('/edit/<int:book_id>', methods=["PUT"])
def update_book(book_id):
    try:
        # Extract book data from the request JSON
        data = request.json
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404

        # Update book fields if provided in the request
        for key, value in data.items():
            setattr(book, key, value)

        # Commit the session to save the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500







# Define the delete book endpoint
@book.route('/delete/<int:book_id>', methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    
    try:
        book_id = Book.query.filter_by(book_id=book_id).first()
        
        if not book_id:
            return jsonify({'error': 'Book not found'}),HTTP_404_NOT_FOUND
        else:
            db.session.delete(book_id)
            db.session.commit()

        return jsonify({'message': 'Book deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR