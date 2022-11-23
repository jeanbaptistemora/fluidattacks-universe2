from db_model import (
    TABLE,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityZeroRiskStatus,
)
from dynamodb.types import (
    Facet,
)

ZR_FILTER_STATUSES = {
    VulnerabilityZeroRiskStatus.CONFIRMED,
    VulnerabilityZeroRiskStatus.REQUESTED,
}

ZR_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="FIN#finding_id",
    sk_alias=(
        "VULN#DELETED#is_deleted#ZR#is_zero_risk#STATE#state_status#VERIF#"
        "verification_status"
    ),
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
