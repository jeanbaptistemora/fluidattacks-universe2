from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

OWNER_INDEX_FACET = Facet(
    attrs=TABLE.facets["credentials_new_metadata"].attrs,
    pk_alias="OWNER#owner",
    sk_alias="CRED#id",
)
