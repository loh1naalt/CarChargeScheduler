from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    role = db.Column(db.String(80), unique=False, nullable=False)
