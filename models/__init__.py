from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import your models so that they are registered with the db instance
from .admin_model import Admin
from .country_model import Country
from .department_model import Department
from .doctype_model import DocType
from .document_model import Document
from .organization_model import Organization
from . report_model import Report
from .staff_model import Staff
from .student_model import Student
