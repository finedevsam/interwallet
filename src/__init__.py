from flask import Flask, redirect
import os

from flask.json import jsonify
from src.auth import auth
from src.merchant import merchant
from src.constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from datetime import timedelta

UPLOAD_FOLDER = os.path.join('uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')

def create_app(test_config=None):
     app = Flask(__name__, 
     instance_relative_config=True)
     
     if test_config is None:
        app.config.from_mapping(
             SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
             SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(db_user, db_pass, db_host, db_name),
             SQLALCHEMY_TRACK_MODIFICATIONS= os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', default=False),
             JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
             JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=120),
             JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=120)
             )
     else:
          app.config.from_mapping(test_config)
          
     db.init_app(app)
    
     JWTManager(app)

     app.register_blueprint(auth)
     app.register_blueprint(merchant)
     
     @app.errorhandler(HTTP_404_NOT_FOUND)
     def hendle_404(e):
        return jsonify({"error": "Not Found"}), HTTP_404_NOT_FOUND
    
    
   #   @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
   #   def hendle_404(e):
   #      return jsonify({"error": "Oop!! We run into an error. Our Engineers are working to to fix it"}), HTTP_500_INTERNAL_SERVER_ERROR
    
     def create_database(app):
        db.create_all(app=app)
        # print("Database Created")
     create_database(app)
     return app
    
    
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)