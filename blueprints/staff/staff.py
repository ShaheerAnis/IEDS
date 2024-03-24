# HEC 
# EMBASSY
# CERITICIATE VERFICATION
# IBCC



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
from flask import send_file, abort,Response
from io import BytesIO
from flask import send_from_directory
from config import Config
    

# Define the admin blueprint.
staff_bp = Blueprint("staff", __name__, template_folder="templates")

# Access the logger defined in main.py
logger = logging.getLogger(__name__)



    
@staff_bp.route('/download_document/<int:document_id>', methods=['GET'])
def download_document(document_id):
    # Retrieve the document from the database based on the document_id
    document = Document.query.get_or_404(document_id)

    # Serve the document file from the file system
    return send_from_directory(Config.UPLOAD_FOLDER, document.Name, as_attachment=True)

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
                session['organization_id'] = user.OrganizationId
                #print(user.OrganizationId)

                if remember_me:
                    session.permanent = True
                else:
                    session.permanent = False
                    
                CertificateVerification_ID = Organization.query.filter(Organization.Name == "CertificateVerification").first().Id
                IBCC_ID = Organization.query.filter(Organization.Name == "IBCC").first().Id
                Embassy_ID = Organization.query.filter(Organization.Name == "Embassy").first().Id
                HEC_ID = Organization.query.filter(Organization.Name == "HEC").first().Id
                Visa_ID = Organization.query.filter(Organization.Name == "Visa").first().Id
                
                
                if user.OrganizationId == CertificateVerification_ID:
                    return redirect(url_for('staff.staff_CertificateVerification'))
                elif user.OrganizationId == IBCC_ID:
                    return redirect(url_for('staff.staff_IBCC'))
                elif user.OrganizationId == Embassy_ID:
                    return redirect(url_for('staff.staff_Embassy'))
                elif user.OrganizationId == HEC_ID:
                    return redirect(url_for('staff.staff_HEC'))
                elif user.OrganizationId == Visa_ID:
                    return redirect(url_for('staff.staff_Visa'))  
                
                else:
                    print("You are not authorized to log in. Please contact your organization.")
                return redirect(url_for('staff.staffRegisteration'))

            else:
                print("You are not authorized to log in. Please contact your organization.")
                return redirect(url_for('staff.staffRegisteration'))
        else:
            print("Login failed. Please try again.")
            return redirect(url_for('staff.staffLogin'))
    else:
        return render_template('staff_dashboard.html')
    
    
# Main Dashboards

@staff_bp.route('/staff_CertificateVerification')
def staff_CertificateVerification():
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    
    user_id = session['student_user_id']
    user = Student.query.get(user_id)
    
    doc_ID = DocType.query.filter(DocType.DocTypeName == "CertificateVerification").first().Id
    documents = db.session.query(Document, Student).join(Student, Document.StudentId == Student.Id).filter(
                        Document.TypeId == doc_ID,
                        Document.AppliedForCA == True,
                        Document.Deleted == False,
                        Document.Status != True
                    ).all()
    
    return render_template('equivalence_documents.html', documents=documents)

@staff_bp.route('/staff_IBCC')
def staff_IBCC():
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    

    
    doc_ID = DocType.query.filter(DocType.DocTypeName == "CertificateVerification").first().Id
    documents = db.session.query(Document, Student).join(Student, Document.StudentId == Student.Id).filter(
                        Document.TypeId == doc_ID,
                        Document.AppliedForIBCC == True,
                        Document.Deleted == False,
                        Document.Status != True
                    ).all()
    return render_template('IBCC_equivalence_documents.html', documents=documents)


@staff_bp.route('/staff_HEC')
def staff_HEC():
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    
    user_id = session['student_user_id']
    user = Student.query.get(user_id)
    
    doc_ID = DocType.query.filter(DocType.DocTypeName == "Bonify").first().Id
    documents = db.session.query(Document, Student).join(Student, Document.StudentId == Student.Id).filter(
                        Document.TypeId == doc_ID,
                        Document.AppliedForHEC == True,
                        Document.Deleted == False,
                        Document.Status != True
                    ).all()
    return render_template('hec_documents.html', documents=documents)

@staff_bp.route('/staff_Embassy')
def staff_Embassy():
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    
    user_id = session['student_user_id']
    user = Student.query.get(user_id)
    
    doc_ID = DocType.query.filter(DocType.DocTypeName == "CertificateVerification").first().Id
    documents = db.session.query(Document, Student).join(Student, Document.StudentId == Student.Id).filter(
                        Document.TypeId == doc_ID,
                        Document.AppliedForEmbassy == True,
                        Document.Deleted == False,
                        Document.Status != True
                    ).all()
    return render_template('embassy_documents.html', documents=documents)

@staff_bp.route('/staff_Visa')
def staff_Visa():
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    
    students_with_visa = Student.query.filter_by(SentVisa=True).all()
    return render_template('VisaList.html', students_with_visa = students_with_visa)
    

@staff_bp.route('/staff_dashboard')
def staff_dashboard():
    # Fetch documents submitted by students, assuming you have a function to do this
    documents = Document.query.filter_by(TypeId='2',
                                         Applied = True).all()
    student_ids = [doc.StudentId for doc in documents]

    # Fetch additional data for the students
    # Assuming you have a Student model and you want to fetch data from that model
    students = Student.query.filter(Student.Id.in_(student_ids)).all()
    
    return render_template('staff_dashboard.html', documents=documents,students=students)

# End Main Dashboards

#Approve Request
@staff_bp.route('/CAapproveReq/<int:document_id>', methods=['GET'])
def CAapproveReq(document_id):
    document = Document.query.get_or_404(document_id)
    if document.Deleted != True:
        document.Deleted = False
        document.AppliedForCA = False
        document.Status = False
        document.AppliedForIBCC = True
        db.session.commit()
        
        return redirect(url_for('staff.staff_CertificateVerification')) 

    else:
        return redirect(url_for('staff.staff_CertificateVerification')) 
    

@staff_bp.route('/IBCCapproveReq/<int:document_id>', methods=['GET'])
def IBCCapproveReq(document_id):
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    document = Document.query.get_or_404(document_id)
    if document.Deleted != True:
        document.Deleted = False
        document.AppliedForCA = False
        document.Status = True
        document.AppliedForIBCC = False
        db.session.commit()
        
        return redirect(url_for('staff.staff_IBCC')) 

    else:
        return redirect(url_for('staff.staff_IBCC')) 
 

#Reject Organization
@staff_bp.route('/IBCCrejectReq/<int:document_id>', methods=['GET'])
def IBCCrejectReq(document_id):
    if 'student_user_id' not in session:
        return render_template('error-403.html')
    document = Document.query.get_or_404(document_id)
    # organizationList = Organization.query.filter_by(Deleted = True) 
    if document.Status != True:
        document.Status = False
        document.Deleted = True
        document.AppliedForIBCC = False
        db.session.commit()
        
        return redirect(request.referrer) 
        
        
    else:
        documents = Document.query.filter_by(TypeId='2',).all()
        student_ids = [doc.StudentId for doc in documents]

    # Fetch additional data for the students
    # Assuming you have a Student model and you want to fetch data from that model
        students = Student.query.filter(Student.Id.in_(student_ids)).all()
        return render_template('staff_dashboard.html', documents=documents,students=students) 
        # return render_template('staff_dashboard.html') 


# @staff_bp.route('/download_document/<int:document_id>')
# def download_document(document_id):
#     # Fetch the document from the database
#     document = Document.query.get(document_id)

#     if not document:
#         abort(404, "Document not found")

#     # Assuming 'document_data' is the column where the file is stored
#     document_data = document.FileLocation  # Replace 'document_data' with your actual column name

#     # You might need to set up a proper filename and mimetype based on your application's logic
#     filename = document.Name  # Replace 'name' with your actual column name
#     mimetype = 'application/pdf'  # Example mimetype, adjust according to your file type

#     # Return the file as an attachment
#     return send_file(document_data, mimetype=mimetype)


@staff_bp.route('/IBCC_staff_dashboard')
def IBCC_staff_dashboard():
    # Fetch documents submitted by students, assuming you have a function to do this
    documents = Document.query.filter_by(
        TypeId='2',
        Deleted = False).all()
    student_ids = [doc.StudentId for doc in documents]

    # Fetch additional data for the students
    # Assuming you have a Student model and you want to fetch data from that model
    students = Student.query.filter(Student.Id.in_(student_ids)).all()
    
    return render_template('IBCC_StaffReg.html', documents=documents,students=students)


@staff_bp.route('/rejectReqIBCC/<int:document_id>', methods=['GET'])
def rejectReqIBCC(document_id):
    document = Document.query.get_or_404(document_id)
    # organizationList = Organization.query.filter_by(Deleted = True) 
    if document.Status != True:
        document.Status = False
        document.Deleted = True
        document.Applied = False
        db.session.commit()
        
        return redirect(url_for('staff.IBCC_staff_dashboard')) 
        
        
    else:
        documents = Document.query.filter_by(
        TypeId='2',
        Deleted = False).all()
        student_ids = [doc.StudentId for doc in documents]

    # Fetch additional data for the students
    # Assuming you have a Student model and you want to fetch data from that model
        students = Student.query.filter(Student.Id.in_(student_ids)).all()
    
        return render_template('IBCC_StaffReg.html', documents=documents,students=students)