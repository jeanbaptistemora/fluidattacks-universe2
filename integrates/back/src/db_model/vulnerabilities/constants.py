from db_model import (
    TABLE,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityZeroRiskStatus,
)
from dynamodb.types import (
    Facet,
)

ACCEPTED_TREATMENT_STATUSES = {
    VulnerabilityTreatmentStatus.ACCEPTED,
    VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
}
ZR_FILTER_STATUSES = {
    VulnerabilityZeroRiskStatus.CONFIRMED,
    VulnerabilityZeroRiskStatus.REQUESTED,
}
RELEASED_FILTER_STATUSES = {
    VulnerabilityStateStatus.SAFE,
    VulnerabilityStateStatus.VULNERABLE,
}

NEW_ZR_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="FIN#finding_id",
    sk_alias=(
        "VULN#DELETED#is_deleted#RELEASED#is_released#ZR#is_zero_risk"
        "#STATE#state_status#VERIF#verification_status"
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

GROUP_INDEX_METADATA = Facet(
    attrs=TABLE.facets["vulnerability_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias="VULN#ZR#is_zero_risk#STATE#state_status#TREAT#is_accepted",
)
