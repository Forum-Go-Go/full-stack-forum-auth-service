# app.py
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

from auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5006))
    app.run(host='0.0.0.0', port=port, debug=True)
