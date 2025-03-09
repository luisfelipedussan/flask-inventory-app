from os import environ

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'mysql://user:password@db:3306/inventory_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY', 'dev')
    
    # Configuración adicional
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 2 