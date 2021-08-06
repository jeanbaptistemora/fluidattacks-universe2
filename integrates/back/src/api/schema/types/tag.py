# None


from api.resolvers.tag import (
    groups,
)
from ariadne import (
    ObjectType,
)

TAG = ObjectType("Tag")
TAG.set_field("groups", groups.resolve)
TAG.set_alias("lastClosedVulnerability", "last_closing_vuln")

# Deprecated fields
TAG.set_field("projects", groups.resolve)
