#!/usr/bin/env python3
"""Helper to authenticate through the Salesforce's OAuth2 flow."""

import json
import urllib.request

print("First create an APP with OAuth2 scope.")
CLIENT_ID = input("Enter your app consumer key: ")
CLIENT_SECRET = input("Enter your app consumer secret: ")
REDIRECT_URI = input("Enter your app redirect uri: ")

print()
print("Please visit this URL and grab the code from the redirection:")
print((
    f"https://login.salesforce.com/services/oauth2/authorize"
    f"?response_type=code&CLIENT_ID={CLIENT_ID}&REDIRECT_URI={REDIRECT_URI}"))

print()
CODE = input("Enter your code: ")

TOKEN_REQUEST = urllib.request.Request(
    "https://login.salesforce.com/services/oauth2/token",
    method="POST",
    data=(
        f"grant_type=authorization_code"
        f"&code={CODE}"
        f"&CLIENT_ID={CLIENT_ID}"
        f"&CLIENT_SECRET={CLIENT_SECRET}"
        f"&REDIRECT_URI={REDIRECT_URI}").encode())
TOKEN_RAW_RESPONSE = urllib.request.urlopen(TOKEN_REQUEST)
token_response: str = TOKEN_RAW_RESPONSE.read().decode('utf-8')

print()
print("This are your required credentials:")
print(json.dumps(token_response, indent=2))
