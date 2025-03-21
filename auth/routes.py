from flask import request, jsonify
from auth import auth_bp
from auth.controllers.auth_controller import login_user, logout_user

@auth_bp.route('/login', methods=['POST'])
def login():
    print("[Auth Routes] /login endpoint called")
    response = login_user(request)
    print("[Auth Routes] /login endpoint returning response:", response)
    return response

@auth_bp.route('/logout', methods=['POST'])
def logout():
    print("[Auth Routes] /logout endpoint called")
    response = logout_user(request)
    print("[Auth Routes] /logout endpoint returning response:", response)
    return response
