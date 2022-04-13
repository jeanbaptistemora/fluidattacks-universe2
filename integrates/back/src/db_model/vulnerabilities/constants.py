from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

FILTER_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="FIN#finding_id",
    sk_alias="VULN#vuln_id#DELETED#is_deleted#ZR#is_zero_risk#STATUS#status",
)
ROOT_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="ROOT#root_id",
    sk_alias="VULN#vuln_id",
)

ASSIGNED_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="USER#email",
    sk_alias="VULN#vuln_id",
)

EVENT_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="EVENT#event_id",
    sk_alias="VULN#vuln_id",
)
