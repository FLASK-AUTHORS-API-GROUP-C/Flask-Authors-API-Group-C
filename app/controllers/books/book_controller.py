from flask import Blueprint,request,jsonify
from app.status_code import  HTTP_404_NOT_FOUND,HTTP_400_BAD_REQUEST,HTTP_409_NOT_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.book_model import Book
from app.models.author_model import Author
from app.models.company_model import Company
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token,jwt_required

# books blue print
books =Blueprint('books',__name__,url_prefix='/api/v1/books')

@books.route("/create", methods=["POST"])
@jwt_required()
def createNewBook():
    # Storing the JSON data coming from the request body
    data = request.get_json()
    title = data.get('title')
    price = data.get('price')
    publication_date = data.get('publication_date')
    description = data.get('description')
    no_of_pages = data.get('no_of_pages')  # This will be a string like "50"
    isbn = data.get('isbn')
    author_id = data.get('author_id')
    company_id = data.get('company_id')

    # Validations for the incoming requests
    if not title or not description or not isbn or not publication_date:
        return jsonify({"error": "Title, description, ISBN, and publication date are required."}), HTTP_400_BAD_REQUEST
    
    # Ensure no_of_pages is a positive integer
    if not no_of_pages:
        return jsonify({"error": "Number of pages is required."}), HTTP_400_BAD_REQUEST

    try:
        no_of_pages = int(no_of_pages)  # Convert to an integer
        if no_of_pages <= 0:
            raise ValueError("Number of pages must be a positive integer.")
    except (ValueError, TypeError):
        return jsonify({"error": "Number of pages must be a positive integer."}), HTTP_400_BAD_REQUEST

    # Validate the price is correct, assuming it's a string with 'shs' prefix
    if not price:
        return jsonify({"error": "Price is required."}), HTTP_400_BAD_REQUEST

    try:
        price = float(price.replace('shs ', '').replace(',', '').strip())  # Clean price string if necessary
    except ValueError:
        return jsonify({"error": "Invalid price format."}), HTTP_400_BAD_REQUEST

    # Check if the incoming book title is similar with the existing one
    if Book.query.filter_by(title=title, author_id=author_id).first() is not None:
        return jsonify({"error": "Book with this title and author_id already exists."}), HTTP_409_NOT_CONFLICT

    # Check if the incoming book isbn is similar with the existing one
    if Book.query.filter_by(isbn=isbn).first() is not None:
        return jsonify({"error": "Book ISBN is already in use."}), HTTP_409_NOT_CONFLICT

    try:
        # Fetching the author and company instances from the database
        author = Author.query.get(author_id)
        company = Company.query.get(company_id)

        # Check if the author and company exist
        if not author:
            return jsonify({"error": "Author not found."}), HTTP_404_NOT_FOUND
        if not company:
            return jsonify({"error": "Company not found."}), HTTP_404_NOT_FOUND

        # Debugging - log the value of no_of_pages before insertion
        print(f"Creating book with {no_of_pages} pages.")  # This will appear in the console

        # Creating a new book with all the necessary fields
        new_book = Book(
            title=title,
            price=price,
            publication_date=publication_date,
            description=description,
            no_of_pages=no_of_pages,
            isbn=isbn,
            author=author,  
            company=company
        )

        db.session.add(new_book)
        db.session.commit()

        # Returning a response with the new book details
        return jsonify({
            "message": title + " has been successfully created.",
            "book": {
                "title": new_book.title,
                "book_id": new_book.id,
                "price": new_book.price,
                "description": new_book.description,
                "no_of_pages": new_book.no_of_pages,
                "publication_date": new_book.publication_date,
                "isbn": new_book.isbn,
                "company": {
                    "name": new_book.company.name,
                    "id": new_book.company.id,
                    "email": new_book.company.email,
                    "contact": new_book.company.contact,
                    "origin": new_book.company.origin,
                    "description": new_book.company.description
                },
                "author": {
                    "first_name": new_book.author.first_name,
                    "last_name": new_book.author.last_name,
                    "email": new_book.author.email,
                    "contact": new_book.author.contact,
                    "password": new_book.author.password,
                    "bio": new_book.author.bio
                }
            }
        }), HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
