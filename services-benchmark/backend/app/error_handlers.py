from flask import jsonify

def handle_exception(e):
    """ Generic handler for uncaught errors. """
    return jsonify({'error': "An internal server error occurred", "details": str(e)}), 500

def register_error_handlers(app):
    app.register_error_handler(Exception, handle_exception)