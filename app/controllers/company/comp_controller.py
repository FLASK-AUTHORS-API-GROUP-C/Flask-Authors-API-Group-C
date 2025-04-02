from flask import Blueprint, request, jsonify
from app.status_code import HTTP_400_BAD_REQUEST,HTTP_409_NOT_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN,HTTP_200_OK
import validators
from app.models.company_model import Company
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

# Company blueprint
companies= Blueprint('company', __name__,url_prefix='/api/v1/companies')

# create  company 

@companies.route("/create",methods=['POST'])
@jwt_required()
def create_company():


# storing requests
    data = request.json
    name = data.get('name')
    author_id = get_jwt_identity()
    origin= data.get('origin')
    description = data.get('description', '')
    


    # validations for the incoming requests
    if not name or not origin or not description:
        return jsonify({"error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    
    
    if Company.query.filter_by(name = name).first() is not None:
        return jsonify({"error":"Company name already in use."}),HTTP_409_NOT_CONFLICT
    
    
    try:
        

        # Creating a new_company
        new_company = Company(name = name, author_id = author_id,description = description, origin=origin)
        db.session.add(new_company)
        db.session.commit()

        # Company  name
        company_name =new_company.get_full_name()

        return jsonify({
            "message":company_name + "has been successfully created as a "+ new_company, 
            "company":{
                "name":new_company.name,
                "id":new_company.id,
                "origin":new_company.origin,
                "description":new_company.description,
                }
                
            }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
#Reading the company  
@companies.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_company(id):
    company = Company.query.get(id)

    if not company:
        return jsonify({"message": "Company not found"}), HTTP_200_OK

    return jsonify({
        "id": company.id,
        "name": company.name,
        "description": company.description,
        "location": company.location,
        "owner_id": company.owner_id
    }), HTTP_200_OK 

# Updating a Company
@companies.route('/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_company(id):
    try:
        current_user_id = get_jwt_identity()
        company = Company.query.get(id)

        if not company:
            return jsonify({"message": "Company not found"}), HTTP_404_NOT_FOUND

        #  Only the owner can update the company
        if company.owner_id != current_user_id:
            return jsonify({"message": "Unauthorized"}), HTTP_403_FORBIDDEN

        data = request.get_json()

        # Update only provided fields
        company.name = data.get('name', company.name)
        company.description = data.get('description', company.description)
        company.location = data.get('location', company.location)

        db.session.commit()

        return jsonify({"message": "Company updated successfully"}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR



@companies.route('token/refresh', methods=['POST'])
@jwt_required()
def refresh_token(id):
    return 




# deleting the company
@companies.route('/delete/<int:company_id>',methods=['DELETE'])
@jwt_required()
def delete_company(company_id):
    try:
        current_author_id = get_jwt_identity()
        logged_in_author =Author.query.filter_by(author_id=current_author_id).first()
        
        


       #Get company by id
        company = Company.query.get(company_id)


        # validations
        if not company:
            return jsonify({"message": "Company not found"}),HTTP_404_NOT_FOUND
        
        if logged_in_author != " author"  or company.author_id != "current_author":
            return jsonify({"error":"you are not authorized to delete this company"}),HTTP_403_FORBIDDEN
        
        else:

        
       

            #delete the associated book 

            for book in company.book:
                db.session.delete(book)

            db.session.delete(company)
            db.session.commit()


        return jsonify({"message": "Company deleted successfully"}),HTTP_200_OK
    except Exception as e:
        db.session.rollback() # rollback in case of an error.
        return jsonify({"error": str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
    
