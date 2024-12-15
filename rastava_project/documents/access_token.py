from django.conf import settings
from docusign_esign import EnvelopesApi, ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, CarbonCopy, SignHere, Tabs
import requests
import time
from datetime import datetime, timedelta
import os
from .models import TokenStorage  # A model to store tokens

client_id = settings.USER_ID
integration_key = settings.INTEGRATION_KEY
client_secret = settings.DOCUSIGN_SECRET_KEY
redirect_uri = settings.DOCUSIGN_REDIRECT_URI
base_path = settings.DOCUSIGN_BASE_URL
authorization_url = f'https://account-d.docusign.com/oauth/auth?response_type=code&scope=signature&client_id={client_id}&redirect_uri={redirect_uri}'
authorization_code = ''
token_url = 'https://account-d.docusign.com/oauth/token'


class TokenManager:
    def __init__(self):
        # Load refresh token from database
        # self.refresh_token = self.get_refresh_token_from_db()
        self.refresh_token = self.get_refresh_token_from_db()
        self.access_token = None
        self.token_expiry = None

    def get_refresh_token_from_db(self):
        try:
            # Fetch the latest refresh token from DB
            token_storage = TokenStorage.objects.latest('id')
            return token_storage.refresh_token
        except TokenStorage.DoesNotExist:
            # Fallback to settings if no token exists in DB
            return settings.REFRESH_TOKEN

    def save_refresh_token_to_db(self, refresh_token):
        # Save the new refresh token in the DB
        TokenStorage.objects.create(refresh_token=refresh_token)

    def use_refresh_token(self):
        url = "https://account-d.docusign.com/oauth/token"
        headers = {
            "Authorization": "Basic ZjVkZTQzOTUtZGZjOC00MTBlLTk4MzktZGU3NDA0YzNhYjNkOmE1ODliZDhhLTVhYmUtNDU5Mi05MTI2LTZhZmI0YjcwZmJjNQ=="
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = requests.post(url, headers=headers, data=data)
        return response


    def get_access_token(self):
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token

        # Exchange refresh token for new access token
        print("Refreshing access token...")
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': settings.USER_ID,
            'client_secret': settings.DOCUSIGN_SECRET_KEY
        }

        response = self.use_refresh_token()
        response.raise_for_status()
        token_data = response.json()

        # Update access token and expiry
        self.access_token = token_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'] - 300)

        # Update refresh token dynamically if provided
        new_refresh_token = token_data.get('refresh_token')
        if new_refresh_token:
            self.refresh_token = new_refresh_token
            self.save_refresh_token_to_db(new_refresh_token)

        return self.access_token
