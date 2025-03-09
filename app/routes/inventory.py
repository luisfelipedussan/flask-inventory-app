from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models.inventory import Inventory
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        items = Inventory.query.all()
        logger.info(f"Retrieved {len(items)} items from database")
        return render_template('index.html', items=items)
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
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
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Inventory.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = float(request.form['price'])
        item.mac_address = request.form['mac_address']
        item.serial_number = request.form['serial_number']
        item.manufacturer = request.form['manufacturer']
        item.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
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