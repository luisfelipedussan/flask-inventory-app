from flask import render_template, request, redirect, url_for, jsonify, flash
from app import app, db
from app.models.inventory import Inventory
import logging
import re

logger = logging.getLogger(__name__)

def validate_mac_address(mac_address):
    """Validar formato de dirección MAC"""
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac_address))

def validate_item(form_data):
    """Validar todos los campos del formulario"""
    errors = []
    
    # Validar nombre
    name = form_data.get('name', '').strip()
    if not name:
        errors.append('El nombre es requerido')
    elif len(name) > 100:
        errors.append('El nombre no puede exceder 100 caracteres')
    
    # Validar precio
    try:
        price = float(form_data.get('price', 0))
        if price <= 0:
            errors.append('El precio debe ser mayor que 0')
    except (ValueError, TypeError):
        errors.append('El precio debe ser un número válido (ejemplo: 99.99)')
    
    # Validar MAC address
    mac_address = form_data.get('mac_address', '').strip()
    if not mac_address:
        errors.append('La dirección MAC es requerida')
    elif not validate_mac_address(mac_address):
        errors.append('Formato de MAC inválido. Use el formato XX:XX:XX:XX:XX:XX')
    
    # Validar número de serie
    serial = form_data.get('serial_number', '').strip()
    if not serial:
        errors.append('El número de serie es requerido')
    elif len(serial) > 50:
        errors.append('El número de serie no puede exceder 50 caracteres')
    
    # Validar fabricante
    manufacturer = form_data.get('manufacturer', '').strip()
    if not manufacturer:
        errors.append('El fabricante es requerido')
    
    return errors

@app.route('/')
def index():
    try:
        items = Inventory.query.all()
        logger.info(f"Retrieved {len(items)} items from database")
        return render_template('index.html', items=items)
    except Exception as e:
        logger.error(f"Error retrieving items: {str(e)}")
        flash('Error al cargar los items del inventario', 'danger')
        return render_template('index.html', items=[])

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            # Validar datos
            errors = validate_item(request.form)
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('add.html', item=request.form), 400

            # Verificar si MAC o serial ya existen
            if Inventory.query.filter_by(mac_address=request.form['mac_address']).first():
                flash('Esta dirección MAC ya existe en el sistema', 'danger')
                return render_template('add.html', item=request.form), 400
            
            if Inventory.query.filter_by(serial_number=request.form['serial_number']).first():
                flash('Este número de serie ya existe en el sistema', 'danger')
                return render_template('add.html', item=request.form), 400

            # Crear nuevo item
            item = Inventory(
                name=request.form['name'],
                price=float(request.form['price']),
                mac_address=request.form['mac_address'],
                serial_number=request.form['serial_number'],
                manufacturer=request.form['manufacturer'],
                description=request.form['description']
            )
            db.session.add(item)
            db.session.commit()
            flash('Item agregado exitosamente', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            logger.error(f"Error adding item: {str(e)}")
            db.session.rollback()
            flash('Error al agregar el item', 'danger')
            return render_template('add.html', item=request.form), 500
            
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Inventory.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Validar datos
            errors = validate_item(request.form)
            if errors:
                for error in errors:
                    flash(error, 'danger')
                return render_template('edit.html', item=item), 400

            # Verificar si MAC o serial ya existen (excluyendo el item actual)
            mac_exists = Inventory.query.filter(
                Inventory.mac_address == request.form['mac_address'],
                Inventory.id != id
            ).first()
            if mac_exists:
                flash('Esta dirección MAC ya existe en el sistema', 'danger')
                return render_template('edit.html', item=item), 400
            
            serial_exists = Inventory.query.filter(
                Inventory.serial_number == request.form['serial_number'],
                Inventory.id != id
            ).first()
            if serial_exists:
                flash('Este número de serie ya existe en el sistema', 'danger')
                return render_template('edit.html', item=item), 400

            # Actualizar item
            item.name = request.form['name']
            item.price = float(request.form['price'])
            item.mac_address = request.form['mac_address']
            item.serial_number = request.form['serial_number']
            item.manufacturer = request.form['manufacturer']
            item.description = request.form['description']
            
            db.session.commit()
            flash('Item actualizado exitosamente', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            logger.error(f"Error updating item: {str(e)}")
            db.session.rollback()
            flash('Error al actualizar el item', 'danger')
            return render_template('edit.html', item=item), 500
    
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    try:
        item = Inventory.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Item eliminado exitosamente', 'success')
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        db.session.rollback()
        flash('Error al eliminar el item', 'danger')
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    flash('El recurso solicitado no existe', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    flash('Error interno del servidor', 'danger')
    return redirect(url_for('index'))

@app.route('/test')
def test():
    return jsonify({'message': 'Test endpoint working!'})

@app.route('/db-test')
def db_test():
    try:
        # Probar crear un item
        test_item = Inventory(
            name='Test Item',
            price=99.99,
            mac_address='00:11:22:33:44:55',
            serial_number='TEST123',
            manufacturer='Test Corp',
            description='Test Description'
        )
        db.session.add(test_item)
        db.session.commit()
        
        # Obtener todos los items
        items = Inventory.query.all()
        
        # Preparar respuesta
        items_list = [{
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'mac_address': item.mac_address,
            'serial_number': item.serial_number,
            'manufacturer': item.manufacturer,
            'description': item.description
        } for item in items]
        
        return jsonify({
            'status': 'success',
            'message': 'Database connection working',
            'items': items_list
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 