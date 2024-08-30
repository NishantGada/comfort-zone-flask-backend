from dbconfig import db

class Toilet(db.Model):
    ToiletID = db.Column(db.Integer, primary_key=True)
    ToiletName = db.Column(db.String(100), nullable=False)
    ToiletDescription = db.Column(db.Text, nullable=True)
    ToiletAddressLine1 = db.Column(db.String(200), nullable=False)
    ToiletAddressLine2 = db.Column(db.String(200), nullable=True)
    ToiletCity = db.Column(db.String(100), nullable=False)
    ToiletState = db.Column(db.String(100), nullable=False)
    ToiletPincode = db.Column(db.String(10), nullable=False)
    ToiletGender = db.Column(db.String(6), nullable=False)  # 'Male', 'Female', 'All'
    ToiletRating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    ToiletCharges = db.Column(db.Float, nullable=False)  # Numerical value
    ToiletComments = db.Column(db.Text, nullable=True)
    ToiletBuildDate = db.Column(db.DateTime, nullable=True, default=None)  # Optional

    def __repr__(self):
        return f'<Toilet {self.ToiletName}>'