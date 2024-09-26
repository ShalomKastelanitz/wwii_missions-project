from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mission(db.Model):
    __tablename__ = 'mission'

    mission_id = db.Column(db.Integer, primary_key=True)
    mission_date = db.Column(db.Date)
    mission_type = db.Column(db.String(100))
    target_country = db.Column(db.String(100))

    # ניתן להוסיף עמודות נוספות לפי הצורך
