from database import db

class Bank(db.Model):
    __tablename__ = "banks"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    
    branches = db.relationship("Branch", backref="bank", lazy=True)
    
    def __repr__(self):
        return f"<Bank(name={self.name})>"

class Branch(db.Model):
    __tablename__ = "branches"
    
    ifsc = db.Column(db.String(11), primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey("banks.id"))
    branch = db.Column(db.String(74))
    address = db.Column(db.String(195))
    city = db.Column(db.String(50))
    district = db.Column(db.String(50))
    state = db.Column(db.String(26))
    
    def __repr__(self):
        return f"<Branch(ifsc={self.ifsc}, branch={self.branch})>"