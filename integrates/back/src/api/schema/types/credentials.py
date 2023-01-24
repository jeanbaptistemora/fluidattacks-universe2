from api.resolvers.credentials import (
    azure_organization,
    is_pat,
    is_token,
    key,
    name,
    oauth_type,
    organization,
    password,
    token,
    type as credential_type,
    user,
)
from ariadne import (
    ObjectType,
)

CREDENTIALS = ObjectType("Credentials")
CREDENTIALS.set_field("azureOrganization", azure_organization.resolve)
CREDENTIALS.set_field("isPat", is_pat.resolve)
CREDENTIALS.set_field("isToken", is_token.resolve)
CREDENTIALS.set_field("key", key.resolve)
CREDENTIALS.set_field("name", name.resolve)
CREDENTIALS.set_field("oauthType", oauth_type.resolve)
CREDENTIALS.set_field("organization", organization.resolve)
CREDENTIALS.set_field("password", password.resolve)
CREDENTIALS.set_field("token", token.resolve)
CREDENTIALS.set_field("type", credential_type.resolve)
CREDENTIALS.set_field("user", user.resolve)
