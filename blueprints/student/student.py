import os
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
from sqlalchemy import or_
from datetime import datetime

from models.country_model import Country , db
from models.department_model import Department
from models.doctype_model import DocType
from models.document_model import Document
from models.organization_model import Organization
from models.report_model import Report
from models.staff_model import Staff
from models.student_model import Student
from .. import mail
from werkzeug.utils import secure_filename

from config import Config


# Define the student blueprint.
student_bp = Blueprint("student", __name__, template_folder="templates")

# Access the logger defined in main.py
logger = logging.getLogger(__name__)




# Add Student
@student_bp.route('/studentRegister', methods=['GET', 'POST'])
def studentRegister():
    if request.method == 'POST':
        # Only student can add new student
        # if 'student_user_id' not in session:
        #     return render_template('error-403.html')
        

        # Get data from form
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        conatct = request.form.get('contact')
        password = request.form.get('password')
        uniRegistrationNumber = request.form.get('uniRegistrationNumber')
        placeOfBirth = request.form.get('placeOfBirth')
        organization_id = request.form.get('organization')
        formdepartment = request.form.get('department')
    

        # Check whether username already exists or not
        user = Student.query.filter_by(UniRegistrationNumber=uniRegistrationNumber).first()
        # user = Student.query.filter(or_(Student.UniRegistrationNumber == uniRegistrationNumber, Student.Username == username)).first()
        if user:
            flash("Username already exists.", "error")
            return redirect(url_for('student.studentRegister'))

        
        if not formdepartment:
            flash("Department does not exist.", "error")
            print("Department does not exist.")
            return redirect(url_for('student.studentRegister'))
        # Create a new student user
        new_user = Student(
            Name=name,
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest(),
            Email=email,
            ContactNumber = conatct,
            UniRegistrationNumber = uniRegistrationNumber,
            PlaceOfBirth = placeOfBirth,
            UniversityId=organization_id,
            DepartmentId = formdepartment
        )

        db.session.add(new_user)
        db.session.commit()

        # Send an email to the new student with their credentials
        # msg = Message("Welcome to the Management Team!",
        #               sender="bizintro1@gmail.com",
        #               recipients=[email])
        # msg.html = f"Hi {name},<br>You have been added as an student to our community.<br>Please login to your account using the following credentials:<br>Username: {username}<br>Password: {password}"

        # mail.send(msg)

        return redirect(url_for('student.show_login'))

    else:
        organizations = Organization.query.filter_by(Deleted=False).all()
        departments = Department.query.filter_by(Deleted=False).all()
        return render_template('register.html', organizations=organizations, departments= departments)


# Login routes


# Route for displaying the login form
@student_bp.route('/studentLogin', methods=['GET'])
def show_login():
    return render_template('studentLogin.html')


# Login
@student_bp.route('/studentLogin', methods=['POST'])
def studentLogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')

        user = Student.query.filter_by(
            Username=username,
            Password=hashlib.sha256(password.encode()).hexdigest(),
        ).first()

        if user:
            session.clear()
            session['student_user_id'] = user.Id
            session['student_username'] = user.Username
            session['admin_user_id'] = None
            session['admin_username'] = None

            if remember_me:
                session.permanent = True
            else:
                session.permanent = False

            return render_template('student_dashboard.html')
        else:
            flash("Login failed. Please try again.")
            return redirect(url_for('student.studentRegister'))
    else:
        return render_template('studentLogin.html')
    


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

@student_bp.route('/completeProfile', methods=['GET', 'POST'])
def completeProfile():
    if request.method == 'POST':
        #Only student can add new student
        if 'student_user_id' not in session:
            return render_template('error-403.html')
        
        user_id = session['student_user_id']
        user = Student.query.get(user_id)
        

        # Get data from form
        countryid = request.form.get('countryid')
        visaid = request.form.get('visaid')
        passportnumber = request.form.get('passportnumber')
        fathername = request.form.get('fathername')
        nicnumber = request.form.get('nicnumber')
        semester = request.form.get('semester')
        address = request.form.get('address')
        
        # Create the upload folder if it doesn't exist
        create_upload_folder()
        print(request.files)
        # Save file to the server
        if 'file' in request.files:
            file = request.files['file']
            print('file got')
            if file and allowed_file(file.filename):
                print("file allowed")
                filename = secure_filename(file.filename)
                file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(file_path)
                # Save the file location to the database
                new_document = Document(Name=filename, UploadDate=datetime.now(), FileLocation=file_path, StudentId=user_id, TypeId = 1)    
                db.session.add(new_document)
                db.session.commit()
                print("doc saved")
        

        user.CountryId = countryid
        user.VisaId = "123"
        user.PassportNumber = passportnumber
        user.FatherName = fathername
        user.NICNumber = nicnumber
        user.Semester = semester
        user.Address = address
        

        db.session.commit()


        return render_template('student_dashboard.html')

    else:
        country = Country.query.filter_by(Deleted=False).all()
        return render_template('completeprofile.html', country = country)
    