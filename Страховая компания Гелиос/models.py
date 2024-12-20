from app_init import *


class Prod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    shortdesc = db.Column(db.String(90), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(20), nullable=False)


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    prod_id = db.Column(db.Integer, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(1000), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
