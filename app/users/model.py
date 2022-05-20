from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255),  unique=True)
    username = db.Column(db.String(45),  unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.Integer)
    user_id = db.Column(db.String(255), nullable=False)
    def __init__(self, username, password, email, user_id):
        self.username = username
        self.password = password
        self.email = email
        self.user_id = user_id

    def __str__(self):
        return "Users(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    # def getByName(self, username):
        # return db.session.query(self).filter(Users.username.like(username)).first()

    def get(self, user_id):
        return self.query.filter_by(user_id=user_id).first()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
