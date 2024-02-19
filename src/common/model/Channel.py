from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, db.ForeignKey('Station.id'), nullable=False)
    occupancy = db.Column(db.Boolean, unique=False, nullable = False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(120), unique=False, nullable=False)

