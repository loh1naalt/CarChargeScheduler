from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    role = db.Column(db.String(80), unique=False, nullable=False)

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    addressname = db.Column(db.String(200), unique=False, nullable=False)
    channels_per_station = db.Column(db.Integer, unique=False, nullable=False)

class UserCar(db.Model):
    __tablename__ = 'user_cars'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    carname = db.Column(db.String(200), unique=False, nullable=False)

class ChannelUserCar(db.Model):
    __tablename__ = 'channel_usercars'
    id = db.Column(db.Integer, primary_key=True)
    id_channel = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    id_user_car = db.Column(db.Integer, db.ForeignKey('user_cars.id'), nullable = False)
    startcharge = db.Column(db.DateTime, unique = False, nullable = False)
    endcharge = db.Column(db.DateTime, unique = False, nullable = False)

class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    occupancy = db.Column(db.Boolean, unique=False, nullable = False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.String(120), unique=False, nullable=False)
    occupiedby = db.Column(db.String(120), unique=False, nullable=False)

class ReportedUsersList(db.Model):
    __tablename__ = 'reported_users_list'
    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    station_address = db.Column(db.String(120), db.ForeignKey('stations.addressname'), nullable=False)
    id_channel = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    additional_tip = db.Column(db.String(1000), unique=False, nullable=False)

