from __init__ import (
    FI_AZUREAD_OAUTH2_KEY,
    FI_AZUREAD_OAUTH2_SECRET,
    FI_GOOGLE_OAUTH2_KEY,
    FI_GOOGLE_OAUTH2_SECRET
)


GOOGLE_CONF_URL = (
    'https://accounts.google.com/.well-known/openid-configuration'
)
GOOGLE_ARGS = dict(
    name='google',
    client_id=FI_GOOGLE_OAUTH2_KEY,
    client_secret=FI_GOOGLE_OAUTH2_SECRET,
    server_metadata_url=GOOGLE_CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

AZURE_AUTHZ_URL = (
    'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)
AZURE_ARGS = dict(
    name='azure',
    client_id=FI_AZUREAD_OAUTH2_KEY,
    client_secret=FI_AZUREAD_OAUTH2_SECRET,
    authorize_url=AZURE_AUTHZ_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
