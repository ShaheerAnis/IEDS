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
admin_bp = Blueprint("admin", __name__, template_folder="templates")

# Access the logger defined in main.py
logger = logging.getLogger(__name__)


# Add Admin
@admin_bp.route('/adminRegister', methods=['GET', 'POST'])
def adminRegister():
    if request.method == 'POST':
        # Only admin can add new Admin
        # if 'admin_user_id' not in session:
        #     return render_template('error-403.html')
        

        # Get data from form
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        conatct = request.form.get('contact')
        password = request.form.get('password')
    

        # Generate a random password
        # characters = string.ascii_letters + string.digits + "!@#$%^&*()_-+"
        # password = ''.join(random.choice(characters) for _ in range(8))

        # Check whether username already exists or not
        user = Admin.query.filter_by(Username=username).first()
        if user:
            flash("Username already exists.", "error")
            return redirect(url_for('admin.adminRegister'))

        # Create a new admin user
        new_user = Admin(
            Name=name,
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest(),
            Email=email,
            ContactNumber = conatct
        )

        db.session.add(new_user)
        db.session.commit()

        # Send an email to the new admin with their credentials
        # msg = Message("Welcome to the Management Team!",
        #               sender="bizintro1@gmail.com",
        #               recipients=[email])
        # msg.html = f"Hi {name},<br>You have been added as an Admin to our community.<br>Please login to your account using the following credentials:<br>Username: {username}<br>Password: {password}"

        # mail.send(msg)

        return redirect(url_for('admin.show_login'))

    else:
        return render_template('register.html')


# Login routes


# Route for displaying the login form
@admin_bp.route('/adminLogin', methods=['GET'])
def show_login():
    return render_template('AdminLogin.html')


# Login
@admin_bp.route('/adminLogin', methods=['POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        user = Admin.query.filter_by(
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest(),
        ).first()

        if user:
            session.clear()
            session['admin_user_id'] = user.Id
            session['admin_username'] = user.Username
            session['student_user_id'] = None
            session['student_username'] = None

            if remember_me:
                session.permanent = True
            else:
                session.permanent = False

            return render_template('admin_dashboard.html')
        else:
            flash("Login failed. Please try again.")
            return redirect(url_for('admin.adminRegister'))
    else:
        return render_template('adminLogin.html')
    
    
    