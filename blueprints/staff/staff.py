# HEC 
# EMBASSY
# CERITICIATE VERFICATION
# IBCC




import secrets
import string
import random
import hashlib
import logging
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    session,
    url_for,
    flash,
    abort,
    jsonify,
)
from flask_mail import Message
from sqlalchemy import func
from models.admin_model import Admin,db
from models.country_model import Country   
from models.department_model import Department
from models.doctype_model import DocType
from models.document_model import Document
from models.organization_model import Organization
from models.report_model import Report
from models.staff_model import Staff
from models.student_model import Student
from .. import mail


# Define the admin blueprint.
staff_bp = Blueprint("staff", __name__, template_folder="templates")

# Access the logger defined in main.py
logger = logging.getLogger(__name__)


# # Add Admin
# @admin_bp.route('/adminRegister', methods=['GET', 'POST'])
# def adminRegister():
#     if request.method == 'POST':
#         # Only admin can add new Admin
#         # if 'admin_user_id' not in session:
#         #     return render_template('error-403.html')
        

#         # Get data from form
#         name = request.form.get('name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         conatct = request.form.get('contact')
#         password = request.form.get('password')
    


#         # Check whether username already exists or not
#         user = Admin.query.filter_by(Username=username).first()
#         if user:
#             flash("Username already exists.", "error")
#             return redirect(url_for('admin.adminRegister'))

#         # Create a new admin user
#         new_user = Admin(
#             Name=name,
#             Username=username,
#             Password=hashlib.sha256(password.encode()).hexdigest(),
#             Email=email,
#             ContactNumber = conatct,    
#             Deleted = False
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return redirect(url_for('admin.show_login'))

#     else:
#         return render_template('adminregister.html')


# # Login routes


# # Route for displaying the login form
# @admin_bp.route('/adminLogin', methods=['GET'])
# def show_login():
#     return render_template('AdminLogin.html')


# # Login
# @admin_bp.route('/adminLogin', methods=['POST'])
# def adminLogin():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         remember_me = request.form.get('remember_me')

#         user = Admin.query.filter_by(
#             Username=username,
#             Password=hashlib.sha256(password.encode()).hexdigest(),
#         ).first()

#         if user:
#             session.clear()
#             session['admin_user_id'] = user.Id
#             session['admin_username'] = user.Username
#             session['student_user_id'] = None
#             session['student_username'] = None

#             if remember_me:
#                 session.permanent = True
#             else:
#                 session.permanent = False

#             return render_template('admin_dashboard.html')
#         else:
#             flash("Login failed. Please try again.")
#             return redirect(url_for('admin.adminRegister'))
#     else:
#         return render_template('adminLogin.html')
    


# #student registratin
# @admin_bp.route('/add_organization', methods=['GET', 'POST'])
# def add_organization():
#     if request.method == 'POST':
#         # Only admin can add new Admin
#         # if 'admin_user_id' not in session:
#         #     return render_template('error-403.html')
        

#         # Get data from form
#         name = request.form.get('name')
        
    
   
#         # Generate a random password
#         # characters = string.ascii_letters + string.digits + "!@#$%^&*()_-+"
#         # password = ''.join(random.choice(characters) for _ in range(8))

#         # Check whether username already exists or not
#         organization = Organization.query.filter_by(Name=name).first()
#         if organization:
#             flash("Organization already exists.", "error")
#             return redirect(url_for('admin.organization'))

#         # Create a new admin user
#         new_organization = Organization(
#             Name=name,
#             Deleted=False,
            
#         )

#         db.session.add(new_organization)
#         db.session.commit()

#         # Send an email to the new admin with their credentials
#         # msg = Message("Welcome to the Management Team!",
#         #               sender="bizintro1@gmail.com",
#         #               recipients=[email])
#         # msg.html = f"Hi {name},<br>You have been added as an Admin to our community.<br>Please login to your account using the following credentials:<br>Username: {username}<br>Password: {password}"

#         # mail.send(msg)

#         return redirect(url_for('admin.add_organization'))

#     else:
#         return render_template('organization.html')
    


# #Delete Organization
# @admin_bp.route('/deleteOrg/<int:organization_id>', methods=['GET'])
# def deleteOrg(organization_id):
#     organization = Organization.query.get_or_404(organization_id)
#     if organization.Deleted != True:
#         organization.Deleted = True
#         db.session.commit()
        
#         return redirect(url_for('admin.organization')) 
        
        
#     else:
#         return render_template('organization.html') 


# #Resstore Organization
# @admin_bp.route('/restoreOrg/<int:organization_id>', methods=['GET'])
# def restoreOrg(organization_id):
#     organization = Organization.query.get_or_404(organization_id)
#     # organizationList = Organization.query.filter_by(Deleted = True) 
#     if organization.Deleted != False:
#         organization.Deleted = False
#         db.session.commit()
        
#         return redirect(url_for('admin.organization')) 
        
        
#     else:
#         return render_template('organization.html') 


# #show organization page
# @admin_bp.route('/organization', methods=['Get'])
# def organization():
#     organizations = Organization.query.all() 
#     return render_template('organization.html', organizations = organizations)
    
    

#Staff Regsitration
@staff_bp.route('/staffRegisteration', methods=['GET', 'POST'])
def staffRegisteration():
    if request.method == 'POST':
        # Only student can add new student
        # if 'student_user_id' not in session:
        #     return render_template('error-403.html')
        

        # Get data from form
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        organization_id = request.form.get('organization')
    

        # Check whether username already exists or not
        user = Staff.query.filter_by(Email=email).first()
        # user = Student.query.filter(or_(Student.UniRegistrationNumber == uniRegistrationNumber, Student.Username == username)).first()
        if user:
            flash("Username already exists.", "error")
            return redirect(url_for('admin.staffRegisteration'))

        
        # Create a new staff user
        new_user = Staff(
            Name=name,
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest(),
            Email=email,
            OrganizationId=organization_id,
            Deleted = False
        )

        db.session.add(new_user)
        db.session.commit()

        # Send an email to the new student with their credentials
        # msg = Message("Welcome to the Management Team!",
        #               sender="bizintro1@gmail.com",
        #               recipients=[email])
        # msg.html = f"Hi {name},<br>You have been added as an student to our community.<br>Please login to your account using the following credentials:<br>Username: {username}<br>Password: {password}"

        # mail.send(msg)

        return redirect(url_for('staff.show_staff_login'))

    else:
        organizations = Organization.query.filter_by(Deleted=False).all()
        # staffmembers = Staff.query.all()
        return render_template('staff_staffRegister.html', organizations=organizations)




@staff_bp.route('/staffLogin', methods=['GET'])
def show_staff_login():
    return render_template('StaffLogin.html')


# Login
@staff_bp.route('/staffLogin', methods=['POST'])
def staffLogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        user = Staff.query.filter_by(
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest(),
        ).first()

        if user:
            # Fetch the organization ID of the user dynamically
            # organization_id = user.OrganizationId  # Assuming you have a relationship defined in the Staff model

            OID = Staff.query.filter_by(
            OrganizationId =  user.OrganizationId).first()
            # Check if the user belongs to a specific organization (replace 'specific_organization_id' with the ID you want to check)
            if OID:
                session.clear()
                session['staff_user_id'] = user.Id
                session['staff_username'] = user.Username
                session['student_user_id'] = None
                session['student_username'] = None

                if remember_me:
                    session.permanent = True
                else:
                    session.permanent = False

                return render_template('staffLogin.html')
            else:
                flash("You are not authorized to log in. Please contact your organization.")
                return redirect(url_for('staff.staffRegisteration'))
        else:
            flash("Login failed. Please try again.")
            return redirect(url_for('staff.staffRegisteration'))
    else:
        return render_template('staffLogin.html')
    


