from flask.json import jsonify
from src.constants.http_status_code import *
from src.database import *
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import  re


class UserManager:
     
     def passwordValidator(self, password):
          """
          Declare Min & Max Length of Password 
          to be use to register on the system
          """
          minPassLength = 8
          maxPassLength = 15


          """Check the Strongness of the password"""
        
          regex = ("^(?=.*[a-z])(?=." + "*[A-Z])(?=.*\\d)" + "(?=.*[-+_!@#$%^&*., ?]).+$")
          p = re.compile(regex)
          """Check the length of the password coming"""
          if len(password) >= minPassLength or len(password) <= maxPassLength:

               """Test the password if it's align to regex structure of Variable Character"""

               if (password == None):
                    return False

               elif(re.search(p, password)):
                    return True
            
               else:
                    return False
          else:
               return False
     
     # Error Response Block
     def erro_response(self, message, status, code):
          data = {
               "code": code,
               "status": "{}".format(status),
               "info": {
                    "message": "{}".format(message)
               }
               
          }
          return jsonify(data), code
     
     # Success Response Block
     def succes_response(self, status, datas, code):
          data = {
               "code": code,
               "status": "{}".format(status),
               "body": datas
          }
          return jsonify(data), code
     
     
     def check_merchant(self, is_mechant):
          if is_mechant == "yes":
               return True
          elif is_mechant == "no":
               return False
          else:
               return None
          
          
     # User Registrations Block
     def user_registration(self, fullname, email, password, is_merchant):
          if self.passwordValidator(password) == False:
               message = "Password must be between 8-15 and contain Uppercase and special character like @!*"
               return self.erro_response(message, status="fail", code=HTTP_400_BAD_REQUEST)
          elif not validators.email(email):
               message = "supplied email is not a valid email"
               return self.erro_response(message, status="fail", code=HTTP_400_BAD_REQUEST)
          elif User.query.filter_by(email=email).first() is not None:
               message = "email is taken"
               return self.erro_response(message, status="fail", code=HTTP_400_BAD_REQUEST)
          
          elif self.check_merchant(is_merchant) == None:
               message = "is_merchant field can either be yes or no"
               return self.erro_response(message, status="fail", code=HTTP_400_BAD_REQUEST)
          else:
               pwd_hash = generate_password_hash(password)
               user = User(fullname=fullname, email=email, is_merchant=self.check_merchant(is_merchant), password=pwd_hash)
               db.session.add(user)
               db.session.commit()
        
               data = {
                    'message': "User Created",
                    'user': {
                         'fullname': fullname,
                         'is_merchant': is_merchant,
                         'email': email
                    }
               }
    
               return self.succes_response(status='success', datas=data, code=HTTP_201_CREATED)
          
     
     # User Login and Token Generation Block
     def login(self, email, password):
          user = User.query.filter_by(email=email).first()
    
          if user:
               is_pass_correct = check_password_hash(user.password, password)
               if is_pass_correct:
                    refresh = create_refresh_token(identity=user.id)
                    access = create_access_token(identity=user.id)
            
                    data = {
                         "user": {
                              "refresh": refresh,
                              "access": access
                         }
                    }
                    return self.succes_response(status="success", datas=data, code=HTTP_200_OK)
               else:
                    message = "Wrong Credentials"
                    
                    return self.erro_response(message, status="fail", code=HTTP_401_UNAUTHORIZED)
        
          else:
               message = "User Not Found"
               return self.erro_response(message, status="fail", code=HTTP_401_UNAUTHORIZED)
            
    
