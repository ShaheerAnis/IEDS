from . import db 

class Organization(db.Model):
    __tablename__ = 'Organization'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Deleted = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"<Organization(Id={self.Id}, Name='{self.Name}')>"
