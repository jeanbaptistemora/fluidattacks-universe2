from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

GSI_2_FACET = Facet(
    attrs=TABLE.facets["forces_execution"].attrs,
    pk_alias="GROUP#name",
    sk_alias="EXEC#execution_date",
)
