from . import db 

class Staff(db.Model):
    __tablename__ = 'Staff'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Username = db.Column(db.String(50))
    Password = db.Column(db.String(1000))
    Email = db.Column(db.String(50))
    OrganizationId = db.Column(db.Integer, db.ForeignKey('Organization.Id'))
    Deleted = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f"<Staff(Id={self.Id}, Discription='{self.Name}')>"
