from flask import Blueprint, request, jsonify, Flask
from flask_jwt_extended.view_decorators import jwt_required
from src.database import *
from src.function.merchant_mgt import MerchantManager
import validators
from flask_jwt_extended import get_jwt_identity
from src.constants.http_status_code import *
from flasgger import swag_from
import os
import string
import random
from werkzeug.utils import secure_filename

use = MerchantManager()

app = Flask(__name__)


UPLOAD_FOLDER = os.path.join('uploads/')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

merchant = Blueprint("account", __name__, url_prefix="/account/merchant")

# Error Response Block
def erro_response(message, status, code):
     data = {
          "code": code,
          "status": "{}".format(status),
          "info": {
               "message": "{}".format(message)
          }
               
     }
     return jsonify(data), code
     
# Success Response Block
def succes_response(status, datas, code):
     data = {
          "code": code,
          "status": "{}".format(status),
          "body": datas
     }
     return jsonify(data), code


def allowed_file(filename):
         return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@merchant.route('/', methods=['GET', 'POST', 'PUT'])
@jwt_required()
def handle_merchant():
     current_user = get_jwt_identity()
     res = ''.join(random.choices(string.digits, k=4))
     merchant_code = str(res)
     if request.method == 'POST':
          merchant_name = request.form.get('merchantName', '')
          merchant_address = request.form.get('merchantAddress', '')
          contact_phone = request.form.get('merchantPhone', '')
          business_email = request.form.get('businessEmail', '')
          image = request.files['image']
          user = User.query.filter_by(id=current_user).first()
          if user.is_merchant == False:
               message = "User is not a merchant"
               return erro_response(message, status='fail', code=HTTP_400_BAD_REQUEST)
          elif Merchant.query.filter_by(business_email=business_email).first() is not None:
               message = "Merchant Email has been used"
               return erro_response(message, status='fail', code=HTTP_400_BAD_REQUEST)
          elif image and allowed_file(image.filename):
               filename = secure_filename(image.filename)
               image.save(os.path.join(app.root_path, "static/uploads/", filename))
               
               merch = Merchant(
                    merchant_code=merchant_code,
                    merchant_name=merchant_name, 
                    merchant_address=merchant_address, 
                    contact_phone=contact_phone,
                    business_email=business_email,
                    user_id=current_user,
                    image=filename
                    )
               db.session.add(merch)
               db.session.commit()
               data = {
                    "id": merch.id,
                    "merchantCode": merch.merchant_code,
                    "merchantName": merch.merchant_name,
                    "merchantAddress": merch.merchant_address,
                    "image": merch.get_image()
               }
               return succes_response(status="success", datas=data, code=HTTP_200_OK)
     
     elif request.method == 'GET':
          merch = Merchant.query.filter_by(user_id=current_user).first()
          if merch is not None:
               data = {
                    "id": merch.id,
                    "merchantCode": merch.merchant_code,
                    "merchantName": merch.merchant_name,
                    "merchantAddress": merch.merchant_address,
                    "contactPhone": merch.contact_phone,
                    "business_email": merch.business_email,
                    "user_id": merch.user_id,
                    "image": merch.get_image(),
                    "created_at": merch.created_at
               }
          else:
               data = []
          return succes_response(status='success', datas=data, code=HTTP_200_OK)
     
     elif request.method == 'PUT':
          merchant_name = request.form.get('merchantName', '')
          merchant_address = request.form.get('merchantAddress', '')
          contact_phone = request.form.get('merchantPhone', '')
          business_email = request.form.get('businessEmail', '')
          image = request.files['image']
          merch = Merchant.query.filter_by(user_id=current_user).first()
          if not merch:
               message = "Oooops!! error occure"
               return erro_response(message, status='fail', code=HTTP_400_BAD_REQUEST)
          else:
               if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.root_path, "static/uploads/", filename))
                    merch.merchant_name = merchant_name
                    merch.merchant_address = merchant_address
                    merch.contact_phone = contact_phone
                    merch.business_email = business_email
                    merch.image = filename
                    db.session.commit()
                    
                    data = {
                         "id": merch.id,
                         "merchantCode": merch.merchant_code,
                         "merchantName": merch.merchant_name,
                         "merchantAddress": merch.merchant_address,
                         "contactPhone": merch.contact_phone,
                         "user_id": merch.user_id,
                         "image": merch.get_image(),
                         "created_at": merch.created_at,
                         "updated_at": merch.updated_at
                    }
                    return succes_response(status='success', datas=data, code=HTTP_200_OK)
               else:
                    message = "Invalid Image Format"
                    return erro_response(message, status='fail', code=HTTP_400_BAD_REQUEST)
     
     else:
          message = "Invalid Request Method"
          return erro_response(message, status='fail', code=HTTP_400_BAD_REQUEST)
     
     

@merchant.route('/apikey/', methods=['GET'])
@jwt_required()
def api_key():
     return use.create_or_update_api_key()