from . import db 
from datetime import datetime
class Student(db.Model):
    __tablename__ = 'Student'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Username = db.Column(db.String(50))
    Password = db.Column(db.String(1000))
    Email = db.Column(db.String(50))
    VisaId = db.Column(db.String(50), nullable=True)
    PassportNumber = db.Column(db.String(100), nullable=True)
    FatherName = db.Column(db.String(100), nullable=True)
    NICNumber = db.Column(db.String(100), nullable=True)
    ContactNumber = db.Column(db.String(50), nullable=True)
    UniRegistrationNumber = db.Column(db.String(50), nullable=True)
    Address = db.Column(db.String(200), nullable=True)
    PlaceOfBirth = db.Column(db.DateTime, nullable=True)
    Semester = db.Column(db.Integer, nullable=True)
    UniversityId = db.Column(db.Integer, db.ForeignKey('Organization.Id'))
    DepartmentId = db.Column(db.Integer, db.ForeignKey('Department.Id'), nullable=True)
    CountryId = db.Column(db.Integer, db.ForeignKey('Country.Id'), nullable=True)
    Deleted = db.Column(db.Boolean, nullable=True)
    SentVisa  = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f"<Student(Id={self.Id}, Discription='{self.Name}')>"
