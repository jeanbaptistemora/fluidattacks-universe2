from __init__ import (
    FI_AZUREAD_OAUTH2_KEY,
    FI_AZUREAD_OAUTH2_SECRET
)


CLIENT_ID = FI_AZUREAD_OAUTH2_KEY
CLIENT_SECRET = FI_AZUREAD_OAUTH2_SECRET

AUTHZ_URL = (
    'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)
CONF_URL = (
    'https://login.microsoftonline.com/common/.well-known/openid-configuration'
)
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
API_BASE_URL = 'https://graph.microsoft.com/'
API_USERINFO_BASE_URL = f'{API_BASE_URL}oidc/userinfo'
SCOPE = 'openid email profile'
