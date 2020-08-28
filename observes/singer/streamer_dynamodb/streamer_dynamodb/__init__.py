# Standard Library
import argparse
import json
import time
from decimal import Decimal
from typing import (
    Any,
    Dict,
    NamedTuple,
    Generator,
)

# Third Library
import boto3
import botocore
from boto3_type_annotations.dynamodb import (
    Client,
    Table,
    ServiceResource,
)
from boto3.session import Session

Connection = NamedTuple('Connection', [('client', Client),
                                       ('resource', ServiceResource)])


def get_connection(aws_access_key_id: str, aws_secret_access_key: str,
                   region_name: str) -> Connection:
    """Creates and access point to DynamoDB.

    :param aws_access_key_id: aws access key.
    :param aws_secret_access_key: aws secret key.
    :param region_name: aws region.
    :return: A tuple with a client and a resource object.
    :rtype: Connection.
    """
    session: Session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name)

    client: Client = session.client('dynamodb')
    resource: ServiceResource = session.resource('dynamodb')

    return Connection(client, resource)


def scan_table(
        table_name: str,
        connection: Connection) -> Generator[Dict[str, Any], None, None]:
    """Return an dynamodb result generator.

    :param table_name: Name of dynamodb table.
    :param connection: A dynamodb connection.
    :yield: DynamoDb scan result.
    :rtype: Generator[Dict, None, None].
    """
    scan_params = {'TableName': table_name, 'Limit': 1000}

    table: Table = connection.resource.Table(table_name)
    has_more = True

    result = {}
    while has_more:
        try:
            result = table.scan(**scan_params)
            yield result
        except (botocore.exceptions.ClientError,
                botocore.exceptions.BotoCoreError):
            time.sleep(10)
            continue

        if result.get('LastEvaluatedKey', None):
            scan_params['ExclusiveStartKey'] = result.get('LastEvaluatedKey')

        has_more = result.get('LastEvaluatedKey', False)


def deserialize(object_: Any) -> Any:
    """Convert an object so it can be serialized to JSON.

    :param object_: Object to deserialize.
    :return: A deserialized object.
    :rtype: Any.
    """
    if isinstance(object_, Decimal):
        object_ = int(object_)
    elif isinstance(object_, dict):
        for key, value in object_.items():
            object_[key] = deserialize(value)
    elif isinstance(object_, (list)):
        for value in object_:
            value = deserialize(value)
    elif isinstance(object_, set):
        object_ = list(object_)
        object_ = deserialize(object_)
    elif isinstance(object_, tuple):
        object_ = list(object_)
        object_ = deserialize(object_)
    else:
        return object_
    return object_


def main() -> None:
    # user interface
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',
                        '--auth',
                        help='JSON authentication file',
                        dest='auth',
                        type=argparse.FileType('r'),
                        required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c',
                       '--conf',
                       help='JSON config file',
                       dest='conf',
                       type=argparse.FileType('r'))
    args = parser.parse_args()

    credentials: Dict[str, str] = json.load(args.auth)
    configuration = json.load(args.conf)

    db_connection = get_connection(
        aws_access_key_id=credentials['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=credentials['AWS_SECRET_ACCESS_KEY'],
        region_name=credentials['AWS_DEFAULT_REGION'])

    for table in configuration.get("tables", []):
        for result in scan_table(table, db_connection):
            for item in result.get('Items', []):
                item = deserialize(item)
                print(json.dumps({"stream": table, "record": item}))


if __name__ == "__main__":
    main()
