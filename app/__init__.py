from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import time
from sqlalchemy.exc import OperationalError
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Crear todas las tablas con reintentos
def init_db(retries=5, delay=2):
    for i in range(retries):
        try:
            with app.app_context():
                db.create_all()
                logger.info("Base de datos inicializada correctamente")
                # Verificar la conexión
                db.session.execute('SELECT 1')
                logger.info("Conexión a la base de datos verificada")
                return True
        except OperationalError as e:
            if i < retries - 1:
                logger.warning(f"Intento {i+1}/{retries}: No se pudo conectar a la base de datos. Error: {str(e)}")
                time.sleep(delay)
                delay *= 2
            else:
                logger.error(f"Error final: No se pudo conectar a la base de datos. Error: {str(e)}")
                return False

# Importar rutas después de crear la aplicación
from app.routes import inventory
from app.models import inventory

# Inicializar la base de datos
if not init_db():
    logger.error("No se pudo inicializar la base de datos")

@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/debug')
def debug_info():
    return jsonify({
        'database_url': app.config['SQLALCHEMY_DATABASE_URI'],
        'debug': app.debug,
        'env': app.env
    })
