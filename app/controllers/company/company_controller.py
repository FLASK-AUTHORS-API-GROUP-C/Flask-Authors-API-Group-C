from flask import Blueprint, request, jsonify
from app.statuscode import HTTP_400_BAD_REQUEST,HTTP_409_NOT_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN,HTTP_200_OK
import validators
from app.models.company_model import Company
from app.extensions import db,bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

# Company blueprint
company= Blueprint('company', _name_,url_prefix='/api/v1/company')

# user registration

@company.route("/register,methods=['POST']")
def register_company():

    data = request.json
    name = data.get('name')
    id = data.get('id')
    email   = data.get('email')
    contact = data.get('contact')
    origin= data.get('origin')
    description = data.get('description', '')if type == "description" else ''
    


    # validations for the incoming requests
    if not name or not  email :
        return jsonify({"error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    if type == 'company' and not description:
        return jsonify({"error":"Enter the company's description."}),HTTP_400_BAD_REQUEST
    
    
    if not validators.email:
        return jsonify({"error":"Email is not valid."}),HTTP_400_BAD_REQUEST
    
    if Company.query.filter_by(email = email).first() is not None:
        return jsonify({"error":"Email address already in use."}),HTTP_409_NOT_CONFLICT
    
    if Company.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Phone number already in use."}),HTTP_409_NOT_CONFLICT
    
    try:
        hashed_password = bcrypt.generate_password_hash('password') # hashing the password

        # Creating a company
        new_company = Company(name = name,id = id,description = description, email = email, contact=contact,
                          contact=contact,)
        db.session.add(Company)
        db.session.commit()

        # Company  name
        company_name =new_company.get_full_name()

        return jsonify({
            "message":company_name + "has been successfully created as a "+ new_company, 
            "user":{
                "name":new_company.name,
                "id":new_company.id,
                "email":new_company.email,
                "contact":new_company.contact,
                "origin":new_company.origin,
                "description":new_company.description,
                }
                
            }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
#Reading the company  
@company.route('/<int:id>', methods=['GET'])
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
@company.route('/update/<int:id>', methods=['PUT'])
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

    
# deleting the company
company.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_company(id):
    try:
        current_company = get_jwt_identity()

        company_to_be_deleted =Company.query.get(id)


        # validations
        if not company_to_be_deleted:
            return jsonify({"message": "Company not found"}),HTTP_404_NOT_FOUND
        
        if company_to_be_deleted.owner_id != current_company:
            return jsonify({"message": "Unauthorized"}),HTTP_403_FORBIDDEN
        
        db.session.delete(company_to_be_deleted)
        db.session.commit()

        return jsonify({"message": "Company deleted successfully"}),HTTP_200_OK
    except Exception as e:
        return jsonify({"error": str(e)}),HTTP_500_INTERNAL_SERVER_ERROR