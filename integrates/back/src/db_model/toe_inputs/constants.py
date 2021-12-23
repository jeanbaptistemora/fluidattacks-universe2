from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

GSI_2_FACET = Facet(
    attrs=TABLE.facets["toe_input_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias=(
        "INPUTS#PRESENT#be_present#COMPONENT#component#ENTRYPOINT#entry_point"
    ),
)
