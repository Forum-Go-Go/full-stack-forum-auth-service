# auth/routes.py
from flask import request, jsonify
from auth import auth_bp
from auth.controllers.auth_controller import login_user, refresh_token, verify_token, logout_user
from auth.decorators.auth_decorators import authorize

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_user(request)

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    return refresh_token(request)

@auth_bp.route('/verify', methods=['GET'])
def verify():
    return verify_token(request)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return logout_user(request)

# Example protected endpoint for testing authorization (same as before)
@auth_bp.route('/admin-test', methods=['GET'])
@authorize(allowed_roles=['admin', 'superadmin'])
def admin_test():
    return jsonify({"message": "You are authorized as an admin."})
