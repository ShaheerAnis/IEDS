from datetime import datetime
from . import db 

class Admin(db.Model):
    __tablename__ = 'Admin'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Username = db.Column(db.String(50))
    Password = db.Column(db.String(50))
    ContactNumber = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<Admin(Id={self.Id}, Username='{self.Username}')>"
