from api.resolvers.credentials import (
    key,
    name,
    password,
    token,
    type as credential_type,
    user,
)
from ariadne import (
    ObjectType,
)

CREDENTIALS = ObjectType("Credentials")
CREDENTIALS.set_field("key", key.resolve)
CREDENTIALS.set_field("name", name.resolve)
CREDENTIALS.set_field("password", password.resolve)
CREDENTIALS.set_field("token", token.resolve)
CREDENTIALS.set_field("type", credential_type.resolve)
CREDENTIALS.set_field("user", user.resolve)
