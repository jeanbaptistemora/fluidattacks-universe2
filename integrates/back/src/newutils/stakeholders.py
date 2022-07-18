from dynamodb.types import (
    Item,
)


def format_invitation_state(invitation: Item, is_registered: bool) -> str:
    if invitation and not invitation["is_used"]:
        return "PENDING"
    if not is_registered:
        return "UNREGISTERED"
    return "REGISTERED"
