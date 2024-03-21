from datetime import datetime
from . import db 

class Department(db.Model):
    __tablename__ = 'Department'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Deleted = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f"<Department(Id={self.Id}, Name='{self.Name}')>"
