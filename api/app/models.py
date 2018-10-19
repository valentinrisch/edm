from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(64), index=True, unique=True)
