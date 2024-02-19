from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class UserCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    carname = db.Column(db.String(200), unique=False, nullable=False)


