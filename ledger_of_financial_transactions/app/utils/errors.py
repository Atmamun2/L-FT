from flask import render_template, request, jsonify
from werkzeug.http import HTTP_STATUS_CODES
from app import db
from app.utils.logger import log_error

def error_response(status_code, message=None):
    """Create a standardized error response."""
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
        'status': 'error',
        'code': status_code
    }
    
    if message:
        payload['message'] = message
    
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    """400 Bad Request"""
    return error_response(400, message)

def unauthorized(message='Please authenticate to access this resource.'):
    """401 Unauthorized"""
    return error_response(401, message)

def forbidden(message='You do not have permission to access this resource.'):
    """403 Forbidden"""
    return error_response(403, message)

def not_found(message='The requested resource was not found.'):
    """404 Not Found"""
    return error_response(404, message)

def method_not_allowed(message='The method is not allowed for the requested URL.'):
    """405 Method Not Allowed"""
    return error_response(405, message)

def page_not_found(e):
    """404 error handler"""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return error_response(404, 'The requested URL was not found on the server.')
    return render_template('errors/404.html'), 404

def forbidden(e):
    """403 error handler"""
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return error_response(403, 'You do not have permission to access this resource.')
    return render_template('errors/403.html'), 403

def internal_server_error(e):
    """500 error handler"""
    db.session.rollback()
    log_error('Server Error', str(e), request)
    
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return error_response(500, 'An unexpected error has occurred. Please try again later.')
    return render_template('errors/500.html'), 500

def handle_exception(e):
    """Global exception handler"""
    db.session.rollback()
    log_error('Unhandled Exception', str(e), request)
    
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return error_response(500, 'An unexpected error has occurred. Please try again later.')
    return render_template('errors/500.html'), 500

def handle_rate_limit_exceeded(e):
    """Rate limit exceeded handler"""
    return error_response(429, f'Rate limit exceeded: {e.description}')

class ValidationError(ValueError):
    pass

class DatabaseError(Exception):
    pass

class ResourceNotFoundError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class RateLimitExceededError(Exception):
    pass

# Register error handlers for custom exceptions
def register_error_handlers(app):
    app.register_error_handler(ValidationError, lambda e: error_response(400, str(e)))
    app.register_error_handler(DatabaseError, lambda e: error_response(500, 'A database error occurred.'))
    app.register_error_handler(ResourceNotFoundError, lambda e: error_response(404, str(e)))
    app.register_error_handler(UnauthorizedError, lambda e: error_response(401, str(e) or 'Authentication required.'))
    app.register_error_handler(ForbiddenError, lambda e: error_response(403, str(e) or 'Insufficient permissions.'))
    app.register_error_handler(RateLimitExceededError, lambda e: error_response(429, str(e) or 'Too many requests.'))
    
    # Register HTTP error handlers
    app.register_error_handler(400, lambda e: error_response(400, 'Bad request.'))
    app.register_error_handler(401, lambda e: error_response(401, 'Authentication required.'))
    app.register_error_handler(403, lambda e: error_response(403, 'Insufficient permissions.'))
    app.register_error_handler(404, lambda e: error_response(404, 'Resource not found.'))
    app.register_error_handler(405, lambda e: error_response(405, 'Method not allowed.'))
    app.register_error_handler(413, lambda e: error_response(413, 'Request entity too large.'))
    app.register_error_handler(429, handle_rate_limit_exceeded)
    app.register_error_handler(500, internal_server_error)
