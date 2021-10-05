from api.resolvers.toe_input import (
    unreliable_root_nickname,
)
from ariadne import (
    ObjectType,
)

TOEINPUTS = ObjectType("ToeInputs")
TOEINPUTS.set_alias("vulnerabilities", "vulns")
TOEINPUTS.set_field("unreliableRootNickname", unreliable_root_nickname.resolve)
