# from keycloak import KeycloakOpenID
# from django.conf import settings


# # Initialize Keycloak instance
# keycloak_openid = KeycloakOpenID(
#     server_url=settings.KEYCLOAK_SERVER_URL,
#     client_id=settings.KEYCLOAK_CLIENT_ID,
#     realm_name=settings.KEYCLOAK_REALM,
#     client_secret_key=settings.KEYCLOAK_CLIENT_SECRET_KEY
# )

# # Function to get user info from token
# def get_user_info(token):
#     return keycloak_openid.userinfo(token)

import requests
from django.conf import settings

class KeycloakService:
    def __init__(self):
        self.server_url = settings.KEYCLOAK_SERVER_URL
        self.realm = settings.KEYCLOAK_REALM
        self.client_id = settings.KEYCLOAK_ADMIN_CLIENT_ID
        self.client_secret = settings.KEYCLOAK_ADMIN_CLIENT_SECRET
        self.token_url = f"{self.server_url}realms/{self.realm}/protocol/openid-connect/token"
        self.user_url = f"{self.server_url}admin/realms/{self.realm}/users"

    def get_admin_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to fetch admin token: {response.text}")

    def create_user(self, username, email, password, first_name='', last_name=''):
        token = self.get_admin_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        user_data = {
            "username": username,
            "enabled": True,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
            "credentials": [
                {
                    "type": "password",
                    "value": password,
                    "temporary": False
                }
            ]
        }
        response = requests.post(self.user_url, headers=headers, json=user_data)
        if response.status_code == 201:
            return {"status": "success", "message": "User created in Keycloak"}
        elif response.status_code == 409:
            return {"status": "exists", "message": "User already exists in Keycloak"}
        else:
            return {"status": "error", "message": response.text}
