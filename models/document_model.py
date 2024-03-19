from datetime import datetime
from . import db 

class Document(db.Model):
    __tablename__ = 'Document'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    UploadDate = db.Column(db.DateTime)
    FileLocation = db.Column(db.String(500))
    Status = db.Column(db.Boolean)
    TypeId = db.Column(db.Integer)
    ContactNumber = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<Document(Id={self.Id}, Name='{self.Name}')>"