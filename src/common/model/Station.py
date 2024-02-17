class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    addressname = db.Column(db.String(200), unique=False, nullable=False)
    channels_per_station = db.Column(db.Integer, unique=False, nullable=False)


