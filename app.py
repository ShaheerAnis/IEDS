import logging
from models import db
from models.admin_model import Admin
from flask import Flask
from config import Config
from flask_mail import Mail
from flask_session import Session
from sqlalchemy import inspect
# from blueprints.user.user import user_bp
from blueprints.student.student import student_bp
from blueprints.admin.admin import admin_bp
# from blueprints.contributor.contributor import contributor_bp

app = Flask(__name__)


app.config.from_object(Config)

#app.jinja_env.autoescape = True
    
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server+Native+Client+11.0%7D%3BServer%3DDESKTOP-EN20RGA%5CSQLEXPRESS%3BDatabase%3DAliMadad%3BTrusted_Connection%3Dyes%3BPort%3D1433"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://' + DESKTOP-EN20RGA + '/' + AliMadad + '?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server"
#app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+17+for+SQL+Server%7D%3BServer%3DDESKTOP-EN20RGA%5CSQLEXPRESS%3BDatabase%3DAliMadad%3BTrusted_Connection%3Dyes%3BPort%3D1433"



# Configure logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log', level=logging.DEBUG, format=log_format)

# Create a logger instance for your application
logger = logging.getLogger(__name__)

#app.config['SECRET_KEY'] = 'your-secret-key'






# Session(app)

mail = Mail()
mail.init_app(app)




    

# app.register_blueprint(user_bp) 
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(admin_bp, url_prefix="/admin")
# app.register_blueprint(contributor_bp, url_prefix="/contributor")

db.init_app(app)

# @app.route('/')
# def adminIndex():
# # Test database connection
#     try:
#         inspector = inspect(db.engine)
#         if 'Admin' in inspector.get_table_names():
#             print("Admin table exists.")
#         else:
#             print("Admin table does not exist.")
#     except Exception as e:
#         print("Error occurred while testing database connection:", e)
    
#     # Add an admin to the database
#     try:
#         # Assuming you're receiving admin details via a POST request, adjust accordingly
#         admin_data = {
#             "Name": "Admin Name",
#             "Email": "admin@example.com",
#             "Username": "admin_username",
#             "Password": "admin_password",
#             "ContactNumber": "00000000000"
#         }
        
#         new_admin = Admin(**admin_data)
#         db.session.add(new_admin)
#         db.session.commit()
        
#         print("Admin added successfully.")
#     except Exception as e:
#         db.session.rollback()  # Rollback the session in case of any error
#         print("Error occurred while adding admin to the database:", e)
    
if __name__ =="__main__":
    app.run(debug=True)
    
