from boto3 import (
    Session,
)
from fa_purity import (
    Cmd,
)
from mypy_boto3_dynamodb import (
    DynamoDBClient,
    DynamoDBServiceResource,
)


def new_session() -> Cmd[Session]:
    # This impure procedure gets inputs (credentials) through the environment
    # e.g. AWS_DEFAULT_REGION
    return Cmd.from_cmd(lambda: Session())


def new_resource(session: Session) -> Cmd[DynamoDBServiceResource]:
    return Cmd.from_cmd(
        lambda: session.resource(
            service_name="dynamodb", use_ssl=True, verify=True
        )
    )


def new_client(session: Session) -> Cmd[DynamoDBClient]:
    return Cmd.from_cmd(lambda: session.client("dynamodb"))
