from .types import (
    OrganizationAccess,
)
from .utils import (
    remove_org_id_prefix,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    AccessAlreadyCreated,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
import simplejson as json  # type: ignore


async def add(*, organization_access: OrganizationAccess) -> None:
    org_access_no_prefix = organization_access._replace(
        email=organization_access.email.lower().strip(),
        organization_id=remove_org_id_prefix(
            organization_access.organization_id
        ),
    )
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": org_access_no_prefix.email,
            "id": org_access_no_prefix.organization_id,
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        **json.loads(json.dumps(org_access_no_prefix)),
    }

    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["organization_access"],
            item=item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise AccessAlreadyCreated.new() from ex
