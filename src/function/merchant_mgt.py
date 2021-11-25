from src.constants.http_status_code import *
from src.database import *
import secrets
from src.function.users import UserManager
from flask_jwt_extended import get_jwt_identity

resp = UserManager()


class MerchantManager:
     
     def create_or_update_api_key(self):
          cur_user_id = get_jwt_identity()
          N = 20
          secret_key = ''.join(secrets.choice(string.ascii_lowercase + string.digits)for i in range(N))
          public_key = ''.join(secrets.choice(string.ascii_lowercase + string.digits)for i in range(N))
          
          user = User.query.filter_by(id=cur_user_id).first()
          if user is not None:
               merch = Merchant.query.filter_by(user_id=cur_user_id).first()
               if merch is not None:
                    api = APIKey.query.filter_by(merchant_id=merch.id, user_id=cur_user_id).first()
                    if api is not None:
                         api.secret_key = "SEC_{}".format(secret_key)
                         api.public_key = "PUB_{}".format(public_key)
                         db.session.commit()
                         data = {
                              "merchantCode": merch.merchant_code,
                              "secret_key":"SEC_{}".format(secret_key),
                              "public_key":"PUB_{}".format(public_key)
                         }
                    else:
                         new_api = APIKey(
                              secret_key="SEC_{}".format(secret_key),
                              public_key="PUB_{}".format(public_key),
                              user_id=cur_user_id,
                              merchant_id=merch.id
                         )
                         db.session.add(new_api)
                         db.session.commit()
                         data = {
                              "merchantCode": merch.merchant_code,
                              "secret_key":"SEC_{}".format(secret_key),
                              "public_key":"PUB_{}".format(public_key)
                         }
                    return resp.succes_response(status='success', datas=data, code=HTTP_200_OK)
               else:
                    return resp.erro_response(message='Kindly complete your merchant profile', status='fail', code=HTTP_401_UNAUTHORIZED)
          else:
               return resp.erro_response(message='error!! User not loggedin', status='fail', code=HTTP_401_UNAUTHORIZED)