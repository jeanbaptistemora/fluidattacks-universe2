from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

GSI_2_FACET = Facet(
    attrs=TABLE.facets["toe_lines_metadata"].attrs,
    pk_alias="GROUP#group_name",
    sk_alias="LINES#PRESENT#be_present#ROOT#root_id#FILENAME#filename",
)
