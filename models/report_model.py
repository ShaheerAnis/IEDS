from . import db 

class Report(db.Model):
    __tablename__ = 'Report'
    
    Id = db.Column(db.Integer, primary_key=True)
    Discription = db.Column(db.String(500))
    StaffId = db.Column(db.Integer, db.ForeignKey('Staff.Id'))
    StudentId = db.Column(db.Integer, db.ForeignKey('Student.Id'))
    Deleted = db.Column(db.Boolean)
    Status = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"<Report(Id={self.Id}, Discription='{self.Discription}')>"
