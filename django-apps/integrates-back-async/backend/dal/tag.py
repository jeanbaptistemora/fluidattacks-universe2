from typing import Dict, List, Union
from decimal import Decimal
import rollbar
from botocore.exceptions import ClientError
from backend.dal.helpers import dynamodb
DYNAMODB_RESOURCE = dynamodb.DYNAMODB_RESOURCE  # type: ignore
TABLE = DYNAMODB_RESOURCE.Table('fi_portfolios')


def update(organization: str, tag: str,
           data: Dict[str, Union[List[str], Decimal]]) -> bool:
    success = False
    primary_keys = {'organization': organization, 'tag': tag}
    try:
        attrs_to_remove = [attr for attr in data if data[attr] is None]
        for attr in attrs_to_remove:
            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='REMOVE #attr',
                ExpressionAttributeNames={'#attr': attr}
            )
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
            del data[attr]

        if data:
            attributes = ['{attr} = :{attr}'.format(attr=attr) for attr in data]
            values = {':{}'.format(attr): data[attr] for attr in data}

            response = TABLE.update_item(
                Key=primary_keys,
                UpdateExpression='SET {}'.format(','.join(attributes)),
                ExpressionAttributeValues=values)
            success = response['ResponseMetadata']['HTTPStatusCode'] == 200
    except ClientError:
        rollbar.report_message('Error: Couldn\'nt update tag', 'error')
    return success


def get_attributes(organization: str, tag: str,
                   attributes: List[str]) -> Dict[str, Union[List[str], str]]:
    item_attrs: Dict[str, Union[List[str], Dict[str, str]]] = {
        'Key': {'organization': organization.lower(), 'tag': tag.lower()},
        'AttributesToGet': attributes
    }
    response = TABLE.get_item(**item_attrs)
    return response.get('Item', {})
