from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ORG_INDEX_METADATA = Facet(
    attrs=TABLE.facets["git_root_metadata"].attrs,
    pk_alias="ORG#name",
    sk_alias="ROOT#uuid",
)
