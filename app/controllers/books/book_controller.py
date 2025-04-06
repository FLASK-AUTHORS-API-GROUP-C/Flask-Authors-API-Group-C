# Creating a new book

from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND
from app.models.book_model import Book
from app.extensions import db
from app.models.author_model import Author
from app.models.company_model import Company
from flask_jwt_extended import jwt_required,get_jwt_identity



 # Creating the book blueprint
book = Blueprint('books', __name__,url_prefix = '/api/v1/books')


#Creating books endpoints
@book.route('/create',methods=['POST'])
@jwt_required()

def create_newbook():

   # storing request data
    data = request.get_json()  # We get the body 

    title = data.get('title')
    pages = data.get('pages')
    price = data.get('price')
    description = data.get('description')
    publication_date = data.get('publication_date')
    image = data.get('image')
    company_id = data.get('company_id')
    author_id = data.get('author_id')
    description = data.get('description')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')
    author_id = data.get('author_id')
    company_id = data.get('company_id')
    author_id = data.get('author_id')
    company = Company.query.get('company_id')
    author = Author.query.get('author_id')




    



#validating the incoming request




    if not title  or not description or not price or not pages :
            return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST
    
    
    if Book.query.filter_by(title=title,author_id=author_id).first() is not None:      
          return jsonify({"error": "Book with this title and user id already exists"}), HTTP_400_BAD_REQUEST

    try:
          
          #creating a new book

          new_book = Book(title=title,pages=pages,image=image,price=price,publication_date=publication_date,company_id=company_id,
                           description=description,created_at=created_at, updated_at=updated_at,
                            author_id=author_id,company=company, author=author )
                        
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
    






# Updating the book endpoint.
@book.route('/edit/<int:book_id>', methods=["PUT"])
def update_book(id):
    try:
        # Extract book data from the request JSON
        data = request.json
        book = Book.query.get(id)
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
def delete_book(id):
    
    try:
        id = Book.query.filter_by(id=id).first()
        
        if not id:
            return jsonify({'error': 'Book not found'}),HTTP_404_NOT_FOUND
        else:
            db.session.delete(id)
            db.session.commit()

        return jsonify({'message': 'Book deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR