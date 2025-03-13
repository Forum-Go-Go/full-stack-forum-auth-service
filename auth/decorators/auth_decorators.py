# auth/decorators/auth_decorators.py
from functools import wraps
from flask import request, jsonify
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET', 'YourSuperSecretKey')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')

def authorize(allowed_roles):
    """
    Decorator to restrict access to endpoints based on user role.
    Checks the JWT in the Authorization header and verifies that the role is permitted.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Authorization header missing or invalid.'}), 401

            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token has expired.'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token.'}), 401

            # Check if the user role in the token is allowed
            if payload.get('role') not in allowed_roles:
                return jsonify({'error': 'Insufficient permissions.'}), 403

            # Optionally attach user information to the request context
            request.user = payload
            return f(*args, **kwargs)
        return wrapper
    return decorator
