from __init__ import (
    FI_BITBUCKET_OAUTH2_KEY,
    FI_BITBUCKET_OAUTH2_SECRET
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
