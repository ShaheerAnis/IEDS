from datetime import datetime
from . import db 

class DocType(db.Model):
    __tablename__ = 'DocType'
    
    Id = db.Column(db.Integer, primary_key=True)
    DocTypeName = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<DocType(Id={self.Id}, DocTypeName='{self.DocTypeName}')>"
