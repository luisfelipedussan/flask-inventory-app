from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import time
from sqlalchemy.exc import OperationalError
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create all tables with retries
def init_db(retries=5, delay=2):
    """Initialize database with retry mechanism"""
    for i in range(retries):
        try:
            with app.app_context():
                db.create_all()
                logger.info("Database initialized successfully")
                # Verify connection
                db.session.execute('SELECT 1')
                logger.info("Database connection verified")
                return True
        except OperationalError as e:
            if i < retries - 1:
                logger.warning(f"Attempt {i+1}/{retries}: Could not connect to database. Error: {str(e)}")
                time.sleep(delay)
                delay *= 2
            else:
                logger.error(f"Final error: Could not connect to database. Error: {str(e)}")
                return False

# Import routes after creating the application
from app.routes import inventory
from app.models import inventory

# Initialize database
if not init_db():
    logger.error("Could not initialize database")

@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/debug')
def debug_info():
    return jsonify({
        'database_url': app.config['SQLALCHEMY_DATABASE_URI'],
        'debug': app.debug,
        'env': app.env
    })
