# # Creating a company cotroller

# from flask import Blueprint,request,jsonify
# from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT
# import validators
# from app.models.company_model import Company
# from app.extensions import db,
# from flask_jwt_extended import get_jwt_identity, jwt_required



# #Creating companies
# companies = Blueprint('auth', __name__,url_prefix='/api/v1/companies')


# #User registration

# @companies.route('/create', methods = ['POST'])
#  # We use ths because we are protecting our end points with a jwt required operator 
# @jwt_required()
# def create_company():
#     data = request.json
#     origin = data.get('origin')
#     description = data.get('description')
#     user_id = data.get('user_id')
#     name = data.get('name')
  
   
# # Validating the data to avoid data redaduncy
#     if not name or not origin or not description:
#         return jsonify({"error: All fileds are required" }),HTTP_400_BAD_REQUEST # This is a bad request and it works when you have left any field unfilled

#     if  Company.query.filter_by(name=name).first() is not None: # This checks whether the email address was already in use
#           return jsonify({"error":"Company name already exists"}),HTTP_409_CONFLICT # This is used whenever there is a violation or something that already exists
    


#    try:
         
#         #Creating the  new  Company
#          new_company = Company(name=name,origin=origin,description=description,)
#          db.session.add(new_company)
#          db.session.commit()

#          # Author name
#          authorname = new_company.get_full_name()


#          return jsonify({
#               'message': authorname + 'has been successfully created as a',
#               'author':{
                   
#                    'first_name':new_company.first_name,
#                    'last_name':new_company.last_name,
#                    'author_contact':new_company.author_contact,
#                    'email_address':new_company.email_addresss,
#                    'password':new_company.password,
#                    'biography':new_company.biography,
#                    'id':new_company.id
                
                 

#               }
#          }),HTTP_201_CREATED
#     except Exception as e:
#          db.session.rollback()
#          return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

    
    
