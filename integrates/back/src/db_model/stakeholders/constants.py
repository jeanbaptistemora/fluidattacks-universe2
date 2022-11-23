from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ALL_STAKEHOLDERS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["stakeholder_metadata"].attrs,
    pk_alias="USER#all",
    sk_alias="USER#email",
)
