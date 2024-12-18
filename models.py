from dbconfig import db
import uuid
from datetime import datetime

class Toilet(db.Model):
    ToiletID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
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
    ToiletAddDate = db.Column(db.DateTime, nullable=True, default=datetime.now)

    def __repr__(self):
        return (
            f"<Toilet(ToiletID={self.ToiletID}, ToiletName='{self.ToiletName}', "
            f"ToiletDescription='{self.ToiletDescription}', ToiletAddressLine1='{self.ToiletAddressLine1}', "
            f"ToiletAddressLine2='{self.ToiletAddressLine2}', ToiletCity='{self.ToiletCity}', "
            f"ToiletState='{self.ToiletState}', ToiletPincode='{self.ToiletPincode}', "
            f"ToiletGender='{self.ToiletGender}', ToiletRating={self.ToiletRating}, "
            f"ToiletCharges={self.ToiletCharges}, ToiletComments='{self.ToiletComments}', "
            f"ToiletBuildDate={self.ToiletBuildDate})>"
        )

    def model_to_dict(obj):
        """
        Convert a SQLAlchemy model object into a dictionary, excluding internal SQLAlchemy state.
        """
        # Extract only the actual columns from the SQLAlchemy model
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}