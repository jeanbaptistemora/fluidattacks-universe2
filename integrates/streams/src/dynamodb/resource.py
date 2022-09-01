from boto3 import (
    Session,
)
from boto3.session import (
    Config,
)
from dynamodb.context import (
    FI_DYNAMODB_HOST,
    FI_DYNAMODB_PORT,
    FI_ENVIRONMENT,
)

ENDPOINT = (
    # FP: the endpoint is hosted in a local environment
    f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}"  # NOSONAR
    if FI_ENVIRONMENT == "dev"
    else None
)
SESSION = Session()
TABLE_NAME = "integrates_vms"

CLIENT = SESSION.client(endpoint_url=ENDPOINT, service_name="dynamodbstreams")
RESOURCE = SESSION.resource(
    config=Config(max_pool_connections=100),
    endpoint_url=ENDPOINT,
    service_name="dynamodb",
)
TABLE_RESOURCE = RESOURCE.Table(TABLE_NAME)
