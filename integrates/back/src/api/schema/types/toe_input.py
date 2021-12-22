from api.resolvers.toe_input import (
    unreliable_root_nickname,
)
from ariadne import (
    ObjectType,
)

TOEINPUT = ObjectType("ToeInput")
TOEINPUT.set_field("unreliableRootNickname", unreliable_root_nickname.resolve)
