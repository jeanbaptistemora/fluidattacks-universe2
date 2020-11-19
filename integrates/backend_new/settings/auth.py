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
AZURE_CONF_URL = (
    'https://login.microsoftonline.com/common/.well-known/openid-configuration'
)
AZURE_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
AZURE_API_BASE_URL = 'https://graph.microsoft.com/'
AZURE_USERINFO_BASE_URL = f'{AZURE_API_BASE_URL}oidc/userinfo'
AZURE_ARGS = dict(
    name='azure',
    api_base_url=AZURE_API_BASE_URL,
    api_userinfo_url=AZURE_USERINFO_BASE_URL,
    token_url=AZURE_TOKEN_URL,
    client_id=FI_AZUREAD_OAUTH2_KEY,
    client_secret=FI_AZUREAD_OAUTH2_SECRET,
    authorize_url=AZURE_AUTHZ_URL,
    server_metadata_url=AZURE_CONF_URL,
    scope='openid email profile'
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
