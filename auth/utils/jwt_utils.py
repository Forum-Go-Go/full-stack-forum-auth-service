# auth/utils/jwt_utils.py
import os
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET', 'YourSuperSecretKey')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRES_IN = int(os.getenv('JWT_EXPIRES_IN', '3600'))  # seconds
REFRESH_TOKEN_EXPIRES_IN = int(os.getenv('REFRESH_TOKEN_EXPIRES_IN', '86400'))  # e.g., 24 hours

def generate_jwt(user):
    payload = {
        'user_id': user.get('id'),
        'role': user.get('role'),
        'verified': user.get('verified'),
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=JWT_EXPIRES_IN)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def generate_refresh_token(user):
    """
    Generates a refresh token with a longer expiration.
    """
    payload = {
        'user_id': user.get('id'),
        'role': user.get('role'),
        'verified': user.get('verified'),
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=REFRESH_TOKEN_EXPIRES_IN)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_jwt(token, token_type='access'):
    """
    Decodes a JWT token. You can extend this to differentiate between access and refresh tokens if needed.
    """
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    print(f"🛠 [DEBUG] Decoded JWT payload: {payload}")  # ✅ 确保 decoded token 包含 verified
    return payload
