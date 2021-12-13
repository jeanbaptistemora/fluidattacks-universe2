from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ROOT_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="ROOT#root_id",
    sk_alias="VULN#vuln_id",
)
