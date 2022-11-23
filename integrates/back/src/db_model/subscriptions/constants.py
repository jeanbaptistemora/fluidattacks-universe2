from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

ALL_SUBSCRIPTIONS_INDEX_METADATA = Facet(
    attrs=TABLE.facets["stakeholder_subscription"].attrs,
    pk_alias="SUBS#all",
    sk_alias="SUBS#frequency",
)

SUBSCRIPTIONS_PREFIX = "SUBS#"
