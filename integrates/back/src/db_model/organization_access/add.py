from .types import (
    OrganizationAccess,
)
from .utils import (
    remove_org_id_prefix,
    remove_stakeholder_prefix,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    OrganizationAccessAlreadyCreated,
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
    org_access_no_prefixes = organization_access._replace(
        email=remove_stakeholder_prefix(organization_access.email),
        organization_id=remove_org_id_prefix(
            organization_access.organization_id
        ),
    )
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["organization_access"],
        values={
            "email": org_access_no_prefixes.email,
            "id": org_access_no_prefixes.organization_id,
        },
    )
    item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        **json.loads(json.dumps(org_access_no_prefixes)),
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
        raise OrganizationAccessAlreadyCreated.new() from ex
