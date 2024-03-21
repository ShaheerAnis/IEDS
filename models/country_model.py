from . import db 

class Country(db.Model):
    __tablename__ = 'Country'
    
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Deleted = db.Column(db.Boolean, nullable=True)
    
    
    def __repr__(self):
        return f"<Country(Id={self.Id}, Name='{self.Name}')>"
