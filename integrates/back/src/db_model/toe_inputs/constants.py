from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

OLD_INPUT_FACET = Facet(
    attrs=TABLE.facets["toe_input_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias="INPUTS#COMPONENT#component#ENTRYPOINT#entry_point",
)
OLD_GSI_2_FACET = Facet(
    attrs=TABLE.facets["toe_input_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias=(
        "INPUTS#PRESENT#be_present#COMPONENT#component#ENTRYPOINT#entry_point"
    ),
)
GSI_2_FACET = Facet(
    attrs=TABLE.facets["toe_input_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias=(
        "INPUTS#PRESENT#be_present#ROOT#root_id#COMPONENT#component#ENTRYPOINT"
        "#entry_point"
    ),
)
