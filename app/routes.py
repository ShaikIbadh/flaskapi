import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from app.utils import allowed_file, error_response
from app.models import get_db_cursor

main_bp = Blueprint('main', __name__)

# Public Route - No Authentication Required
@main_bp.route('/public', methods=['GET'])
def public_items():
    """Public route that lists all items (NO token required)."""
    cursor = get_db_cursor()
    cursor.execute("SELECT id, name, description FROM items")
    rows = cursor.fetchall()
    cursor.close()

    items = [{'id': item_id, 'name': name, 'description': description} for item_id, name, description in rows]

    return jsonify(items), 200

# File Upload Route
@main_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return error_response('No file part in the request', 400)

    file = request.files['file']
    if file.filename == '':
        return error_response('No file selected for upload', 400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201

    return error_response('Invalid file type. Only JPG, JPEG, PNG, PDF, and TXT files are allowed.', 400)

# CRUD Operations

# Create Item
@main_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return error_response("Name and description are required.", 400)

    cursor = get_db_cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (name, description))
    cursor.connection.commit()
    cursor.close()

    return jsonify({'message': 'Item created successfully'}), 201

# Read All Items
@main_bp.route('/items', methods=['GET'])
@jwt_required()
def get_all_items():
    cursor = get_db_cursor()
    cursor.execute("SELECT id, name, description FROM items")
    rows = cursor.fetchall()
    cursor.close()

    items = [{'id': item_id, 'name': name, 'description': description} for item_id, name, description in rows]

    return jsonify(items), 200

# Read Item by ID
@main_bp.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item_by_id(item_id):
    cursor = get_db_cursor()
    cursor.execute("SELECT id, name, description FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()

    if not item:
        return error_response('Item not found', 404)

    return jsonify({'id': item[0], 'name': item[1], 'description': item[2]}), 200

# Update Item
@main_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return error_response("Name and description are required.", 400)

    cursor = get_db_cursor()
    cursor.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", (name, description, item_id))
    if cursor.rowcount == 0:
        cursor.close()
        return error_response("Item not found or no changes made.", 404)

    cursor.connection.commit()
    cursor.close()

    return jsonify({'message': 'Item updated successfully'}), 200

# Delete Item
@main_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    cursor = get_db_cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    if cursor.rowcount == 0:
        cursor.close()
        return error_response("Item not found.", 404)

    cursor.connection.commit()
    cursor.close()

    return jsonify({'message': 'Item deleted successfully'}), 200
