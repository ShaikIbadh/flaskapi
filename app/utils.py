from flask import jsonify

# Standardized error response
def error_response(message, status_code):
    return jsonify({'error': message}), status_code
    
# Check if uploaded file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'pdf', 'txt'}
