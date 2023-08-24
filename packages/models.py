from packages import db

class Product(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(length=20),nullable=False,unique=True)
    category = db.Column(db.String(length=20),nullable=False)
    image = db.Column(db.String(length=20),nullable=False,unique=True)
    price = db.Column(db.Integer(),nullable=False)
    description = db.Column(db.String(length=1024),nullable=False,unique=True)

class Category(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=20),nullable=False,unique=True)
    image = db.Column(db.String(length=20),nullable=False,unique=True)