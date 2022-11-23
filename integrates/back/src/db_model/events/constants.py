from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

GSI_2_FACET = Facet(
    attrs=TABLE.facets["event_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias="EVENT#SOLVED#is_solved",
)
