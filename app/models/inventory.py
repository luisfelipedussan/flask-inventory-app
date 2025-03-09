from app import db
from sqlalchemy import DECIMAL

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    mac_address = db.Column(db.String(17), unique=True)
    serial_number = db.Column(db.String(50), unique=True)
    manufacturer = db.Column(db.String(100))
    description = db.Column(db.Text)
    text_field = db.Column(db.Text)
    date_field = db.Column(db.DateTime)
    boolean_field = db.Column(db.Boolean)
    decimal_field = db.Column(DECIMAL(10,2))

    def __repr__(self):
        return f'<Inventory {self.name}>' 