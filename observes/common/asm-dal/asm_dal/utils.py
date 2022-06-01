from boto3 import (
    Session,
)
from dataclasses import (
    dataclass,
)
from mypy_boto3_dynamodb import (
    DynamoDBClient,
    DynamoDBServiceResource,
)


@dataclass(frozen=True)
class AwsCreds:
    key_id: str
    secret: str
    session: str

    def __str__(self) -> str:
        return "[aws masked creds]"

    def __repr__(self) -> str:
        return "[aws masked creds]"


def new_session(creds: AwsCreds) -> Session:
    return Session(
        aws_access_key_id=creds.key_id,
        aws_secret_access_key=creds.secret,
        aws_session_token=creds.session,
        region_name="us-east-1",
    )


def new_resource(session: Session) -> DynamoDBServiceResource:
    return session.resource(service_name="dynamodb", use_ssl=True, verify=True)


def new_client(session: Session) -> DynamoDBClient:
    return session.client("dynamodb")
