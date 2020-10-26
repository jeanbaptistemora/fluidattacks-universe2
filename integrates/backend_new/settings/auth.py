from __init__ import (
    FI_AZUREAD_OAUTH2_KEY,
    FI_AZUREAD_OAUTH2_SECRET,
    FI_BITBUCKET_OAUTH2_KEY,
    FI_BITBUCKET_OAUTH2_SECRET,
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

BITBUCKET_AUTZ_URL = 'https://bitbucket.org/site/oauth2/authorize'
BITBUCKET_ACCESS_TOKEN_URL = 'https://bitbucket.org/site/oauth2/access_token'
BITBUCKET_API_BASE_URL = 'https://api.bitbucket.org/2.0/'
BITBUCKET_USERINFO_ENDPOINT_URL = 'https://api.bitbucket.org/2.0/user'
BITBUCKET_ARGS = dict(
    name='bitbucket',
    api_base_url=BITBUCKET_API_BASE_URL,
    access_token_url=BITBUCKET_ACCESS_TOKEN_URL,
    userinfo_endpoint=BITBUCKET_USERINFO_ENDPOINT_URL,
    client_id=FI_BITBUCKET_OAUTH2_KEY,
    client_secret=FI_BITBUCKET_OAUTH2_SECRET,
    authorize_url=BITBUCKET_AUTZ_URL,
    client_kwargs={
        'scope': 'email account'
    }
)
