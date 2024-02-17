class ChannelUserCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_channel = (db.Integer, db.ForeignKey('Channel.id'), nullable = False)
    id_user = (db.Integer, db.ForeignKey('User.id'), nullable = False)
    id_user_car = (db.Integer, db.ForeignKey('UserCar.id', nullable = False)
    startcharge = (db.DateTime, unique = False, nullable = False)
    endcharge = (db.DateTime, unique = False, nullable = False)
    

