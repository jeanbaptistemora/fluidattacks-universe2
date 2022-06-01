from db_model import (
    TABLE,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Facet,
)

DEFAULT_MAX_SEVERITY = Decimal("10.0")
DEFAULT_MIN_SEVERITY = Decimal("0.0")
ORGANIZATION_ID_PREFIX = "ORG#"


ALL_ORGANIZATIONS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["organization_metadata"].attrs,
    pk_alias="ORG#all",
    sk_alias="ORG#id",
)
