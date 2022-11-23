from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ME_DRAFTS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["finding_metadata"].attrs,
    pk_alias="USER#email",
    sk_alias="FIN#id",
)
