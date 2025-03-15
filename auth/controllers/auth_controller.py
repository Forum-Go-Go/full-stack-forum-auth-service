# auth/controllers/auth_controller.py
import os
import datetime
import jwt
from flask import jsonify, request
from werkzeug.security import check_password_hash  # Use this instead of bcrypt.checkpw
from auth.services.user_service_client import get_user_by_email
from auth.utils.jwt_utils import generate_jwt, decode_jwt, generate_refresh_token
from dotenv import load_dotenv

load_dotenv()  # Ensure environment variables are loaded

def login_user(request_obj):
    print("🚀 [Auth Controller] login_user called - BEFORE READING REQUEST DATA")
    
    try:
        print("📌 [Auth Controller] Reading JSON Data from Request")
        data = request_obj.get_json(silent=True)  # Force parsing JSON even if headers are missing
        print(f"📥 [Auth Controller] Received login request data: {data}")
    except Exception as e:
        print(f"❌ [Auth Controller] Error parsing request JSON: {e}")
        return jsonify({'error': 'Invalid JSON format'}), 400

    email = data['email']
    password = data['password']

    # Retrieve user data from the User Service
    print(f"🔍 [Auth Controller] Fetching user data from User Service for email: {email}")
    user = get_user_by_email(email)

    if not user:
        print("❌ [Auth Controller] No user found for given email")
        return jsonify({'error': 'Invalid credentials.'}), 401

    print(f"✅ [Auth Controller] User found: {user}")

    # Retrieve the stored hashed password
    stored_hash = user.get('hashedPassword')
    if not stored_hash:
        print(f"❌ [Auth Controller] User record is missing the hashed password: {user}")
        return jsonify({'error': 'User record is incomplete.'}), 500

    # Validate password
    print(f"🔑 [Auth Controller] Verifying password for user {email}")
    if not check_password_hash(stored_hash, password):
        print("❌ [Auth Controller] Password verification failed")
        return jsonify({'error': 'Invalid credentials.'}), 401

    print("✅ [Auth Controller] Password verification successful")

    # Extract role and verified status from user data
    user_role = user.get('type', 'user')  # Default to 'user' if role is missing
    user_verified = bool(user.get('verified', 0))  # Convert to boolean (0 → False, 1 → True)

    print(f"🔍 [Auth Controller] Extracted Role: {user_role}, Verified: {user_verified}")

    # Prepare user payload for JWT
    user_payload = {
        'id': user.get('id'),
        'role': user_role,
        'verified': user_verified
    }

    # Generate JWT and refresh token
    print("🔐 [Auth Controller] Generating JWT and refresh token")
    token = generate_jwt(user_payload)  # Ensure generate_jwt now includes role & verified
    refresh = generate_refresh_token(user_payload)

    print("✅ [Auth Controller] JWT and refresh token generated successfully")
    
    response = {
        'token': token,
        'refreshToken': refresh
    }

    print(f"📤 [Auth Controller] Returning successful login response: {response}")
    return jsonify(response), 200



def refresh_token(request_obj):
    """
    This endpoint accepts a refresh token and returns a new JWT.
    """
    data = request_obj.get_json()
    if not data or 'refreshToken' not in data:
        return jsonify({'error': 'Refresh token is required.'}), 400

    refresh_token_value = data['refreshToken']
    try:
        payload = decode_jwt(refresh_token_value, token_type='refresh')
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token has expired.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid refresh token.'}), 401

    # Construct a user dictionary using the payload
    user = {'id': payload.get('user_id'), 'role': payload.get('role')}
    new_token = generate_jwt(user)
    return jsonify({'token': new_token}), 200

def verify_token(request_obj):
    """
    Verifies the access token sent in the Authorization header.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid Authorization header.'}), 401

    token = auth_header.split(' ')[1]
    try:
        payload = decode_jwt(token)
        return jsonify({'message': 'Token is valid', 'decoded': payload}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token.'}), 401

def logout_user(request_obj):
    """
    Simulate logout by returning a success message.
    In a real system, you might implement token blacklisting.
    """
    return jsonify({'message': 'Logout successful. Please discard your token.'}), 200
