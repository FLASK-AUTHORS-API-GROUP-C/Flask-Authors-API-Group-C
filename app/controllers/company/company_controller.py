from flask import Blueprint, request, jsonify
from app.models.author_model import Author
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_403_FORBBIDEN,HTTP_409_NOT_CONFLICT,HTTP_409_CONFLICT
from app.models.company_model import Company
from app.controllers.auth.auth_controller import auth
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

# Company blueprint
company= Blueprint('company', __name__,url_prefix='/api/v1/company')


# Creating a company

@company.route("/create",methods=['POST'])
@jwt_required()
def register_company():


# Storing request values an include everything that you mentioned in your model
    data = request.json # Getting the body
    name = data.get('name')
    origin= data.get('origin')
    description = data.get('description', '')
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')
    author = data.get('author')
    author_id = data.get('author_id')
    
    


    # validations for the incoming requests
    if not name or not  origin or not description:
        return jsonify({"error":"All fields are required."}),HTTP_400_BAD_REQUEST
    
    if Company.query.filter_by(name = name).first() is not None:
        return jsonify({"error":"Company name  address already in use."}),HTTP_409_NOT_CONFLICT
    

    
    try:
        
        # Creating a instance (company) and ensure to include everything that you mentioned in your model
        new_company = Company(name = name,description = description,origin=origin,
                              created_at=created_at,updated_at=updated_at,author=author,author_id=author_id)
        db.session.add(new_company)
        db.session.commit()

    

        return jsonify({
            "message":new_company.name + "has been successfuly created as a new company", 
            "user":{
                
                "id":new_company.id,
                "name":new_company.name,
                "origin":new_company.origin,
                "description":new_company.description,
                }
                
            }),HTTP_201_CREATED


    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    





    
#Getting the company  by id
@company.route('/company/<int:id>', methods=['GET'])
@jwt_required()
def get_company(id):
    company = Company.query.get(id)

    if not company:
        return jsonify({"message": "Company not found"}), HTTP_404_NOT_FOUND

    return jsonify({
        "id": company.id,
        "name": company.name,
        "description": company.description,
        "origin": company.origin,
    }), HTTP_200_OK 






# Getting all companies

@company.route('/companies')
def get_all_companies():

    try:

        all_companies = Company.query.all()
        company_data = []

        for company in all_companies:
            company_information = {
                 "id":company.id,
                "name":company.name,
                "origin":company.origin,
                "description":company.description
            }

            company_data.append(company_information)

        return jsonify({
            'message': 'All companies have been successifully retrieved',
            'total': len(company_data),
            'companies': company_data
        })


    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR












# Updating a Company
@company.route('/update/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def updateCompanyDetails(id):



    try:
        current_user_id = get_jwt_identity()
        loggedInUser = Author.query.filter_by(id=current_user_id).first()


       # updating the request by id parameter
        company = Company.query.filter_by(id=id).first()


        if not auth:
            return jsonify({"message": "Company not found"}), HTTP_404_NOT_FOUND

        #  Only the owner can update the company
        elif auth.type!='admin' and auth.author_id!=current_user_id:
            return jsonify({"message": "You are not authorized to update the company details"}), HTTP_403_FORBBIDEN

        else:
            # Store request data
            name = request.get_json().get('name',company.name)
            origin = request.get_json().get('origin',company.origin)
            description = request.get_json().get('description',company.description)


            if name != company.name and auth.query.filter_by(name=name).first():
                return jsonify({
                    'error':'Name already in use'
                    }),HTTP_409_CONFLICT
            


            company.name = name
            company.origin = origin
            company.description = description


            
            db.session.commit()

            # Update now
            
            return jsonify({
                "message":name + " 's details have been successfully updated",
                'User':{
                            "id": company.id,
        "name": company.name,
        "description": company.description,
        "origin": company.origin,
                    
                    
                }
            })
        


    except Exception as e:
        return jsonify({
            "error": str(e)
            }), HTTP_500_INTERNAL_SERVER_ERROR





    
# deleting the company by id
@company.route('/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_company(id):
    try:
        # current_company = get_jwt_identity()
    
        company_to_be_deleted =Company.query.get(id)


        # validations
        if not company_to_be_deleted:
            return jsonify({"message": "Company not found"}),HTTP_404_NOT_FOUND
        
        # if company_to_be_deleted.author_id != current_company:
        #     return jsonify({"message": "Unauthorized"}),HTTP_403_FORBBIDEN
        
        else:

           db.session.delete(company_to_be_deleted)
           db.session.commit()

        return jsonify({"message": "Company deleted successfully"}),HTTP_200_OK
    except Exception as e:
        return jsonify({"error": str(e)}),HTTP_500_INTERNAL_SERVER_ERROR



