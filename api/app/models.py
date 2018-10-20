from app import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(64), index=True, unique=True)
    toxic = db.Column(db.String(64))

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)