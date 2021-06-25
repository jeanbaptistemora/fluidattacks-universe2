from context import (
    FI_AZUREAD_OAUTH2_KEY,
    FI_AZUREAD_OAUTH2_SECRET,
)

API_BASE_URL = "https://graph.microsoft.com/"
API_USERINFO_BASE_URL = f"{API_BASE_URL}oidc/userinfo"
AUTHZ_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
CLIENT_ID = FI_AZUREAD_OAUTH2_KEY
CLIENT_SECRET = FI_AZUREAD_OAUTH2_SECRET
SCOPE = "openid email profile"
TOKEN_URL = (
    "https://login.microsoftonline.com/common/oauth2/v2.0/token"  # nosec
)
