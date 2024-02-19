from flask_sqlalchemy import SQLAlchemy
class ChannelUserCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_channel = db.Column(db.Integer, db.ForeignKey('Channel.id'), nullable = False)
    id_user = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    id_user_car = db.column(db.Integer, db.ForeignKey('UserCar.id'), nullable = False)
    startcharge = db.Column(db.DateTime, unique = False, nullable = False)
    endcharge = db.Column(db.DateTime, unique = False, nullable = False)
    

