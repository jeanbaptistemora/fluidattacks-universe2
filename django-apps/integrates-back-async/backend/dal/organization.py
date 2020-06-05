import uuid
from typing import Optional, List
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

import rollbar
from backend.dal.helpers import dynamodb
from backend.exceptions import InvalidOrganization
from backend.typing import (
    Organization as OrganizationType
)

DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('integrates')


def _map_keys_to_domain(org: OrganizationType) -> OrganizationType:
    """
    Map DynamoDB keys to a human-readable form
    """
    mapping = {
        'pk': 'id',
        'sk': 'name'
    }
    mapped_org = {key: org[key] for key in org if key not in mapping}
    mapped_org.update({mapping[key]: org[key] for key in org if key in mapping})
    return mapped_org


def _map_keys_to_dal(org: OrganizationType) -> OrganizationType:
    """
    Map domain keys to its DynamoDB representation
    """
    mapping = {
        'id': 'pk',
        'name': 'sk'
    }
    mapped_org = {key: org[key] for key in org if key not in mapping}
    mapped_org.update({mapping[key]: org[key] for key in org if key in mapping})
    return mapped_org


def _map_attributes_to_dal(attrs: List[str]) -> List[str]:
    """
    Map domain attributes to its DynamoDB representation
    """
    mapping = {
        'id': 'pk',
        'name': 'sk'
    }
    mapped_attrs = [attr for attr in attrs if attr not in mapping]
    mapped_attrs.extend([mapping[attr] for attr in attrs if attr in mapping])
    return mapped_attrs


def create(organization_name: str) -> OrganizationType:
    """
    Create an organization and returns its key
    """
    if exists(organization_name):
        raise InvalidOrganization()

    new_item = {'pk': 'ORG#{}'.format(str(uuid.uuid4())),
                'sk': organization_name.lower()}
    try:
        TABLE.put_item(Item=new_item)
    except ClientError as ex:
        rollbar.report_message('Error: Couldn\'nt create organization',
                               'error', extra_data=ex, payload_data=locals())
    return _map_keys_to_domain(new_item)


def exists(org_name: str) -> bool:
    """
    Returns True if the organization key exists
    """
    org = get(org_name)
    resp = False
    if org:
        resp = True
    return resp


def get(org_name: str,
        attributes: List[str] = None) -> Optional[OrganizationType]:
    """
    Get an organization info given its name
    Return specified attributes or all if not setted
    """
    key_exp = Key('sk').eq(org_name) & \
        Key('pk').begins_with('ORG#')
    query_attrs = {
        'KeyConditionExpression': key_exp,
        'IndexName': 'gsi-1',
        'Limit': 1
    }
    if attributes:
        projection = ','.join(_map_attributes_to_dal(attributes))
        query_attrs['ProjectionExpression'] = projection
    response = TABLE.query(**query_attrs).get('Items', [])
    org = None
    if response:
        org = _map_keys_to_domain(response[0])
    return org


def get_or_create(organization_name: str) -> OrganizationType:
    """
    Return an organization, even if it does not exists,
    in which case it will be created
    """
    org = get(organization_name, ['id', 'name'])
    if not org:
        org = create(organization_name)
    return org
