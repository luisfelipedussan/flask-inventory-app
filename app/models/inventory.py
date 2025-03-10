from app import db
from sqlalchemy import DECIMAL

class Inventory(db.Model):
    """
    Inventory Model
    
    Represents an item in the inventory system with its properties.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the item (max 100 chars)
        price (float): Price of the item (must be positive)
        mac_address (str): MAC address (format XX:XX:XX:XX:XX:XX)
        serial_number (str): Unique serial number (max 50 chars)
        manufacturer (str): Manufacturer name
        description (str): Optional item description
    """
    
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