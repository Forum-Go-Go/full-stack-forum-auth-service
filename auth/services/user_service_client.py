# auth/services/user_service_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Make sure USER_SERVICE_URL points to the base URL of the user service (e.g., http://localhost:5001)
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5001')

def get_user_by_email(email):
    """
    Sends a GET request to the User Service's /users/search endpoint to fetch user data by email.
    """
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/search", params={"email": email})
        # print("Response status:", response.status_code)
        # print("Response content:", response.text)
        if response.status_code == 200:
            return response.json()  # Expected to return a user object
        else:
            return None
    except Exception as e:
        print("Error fetching user data:", e)
        return None
