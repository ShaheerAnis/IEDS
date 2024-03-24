from datetime import datetime
from . import db 

class Document(db.Model):
    __tablename__ = 'Document'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(4000))
    UploadDate = db.Column(db.DateTime)
    FileLocation = db.Column(db.String(500))
    Status = db.Column(db.Boolean)
    TypeId = db.Column(db.Integer, db.ForeignKey('DocType.Id'))
    StudentId = db.Column(db.Integer, db.ForeignKey('Student.Id'))
    Deleted = db.Column(db.Boolean, nullable=True)  
    AppliedForCA = db.Column(db.Boolean, nullable=True)
    AppliedForIBCC = db.Column(db.Boolean, nullable=True)
    AppliedForHEC = db.Column(db.Boolean, nullable=True)
    AppliedForEmbassy = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f"<Document(Id={self.Id}, Name='{self.Name}')>"
