from context import (
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
    FI_DYNAMODB_HOST,
    FI_DYNAMODB_PORT,
    FI_ENVIRONMENT,
)

RESOURCE_OPTIONS = {
    "aws_access_key_id": FI_AWS_DYNAMODB_ACCESS_KEY,
    "aws_secret_access_key": FI_AWS_DYNAMODB_SECRET_KEY,
    "aws_session_token": FI_AWS_SESSION_TOKEN,
    "endpoint_url": (
        # FP: the endpoint is hosted in a local environment
        f"http://{FI_DYNAMODB_HOST}:{FI_DYNAMODB_PORT}"  # NOSONAR
        if FI_ENVIRONMENT == "development"
        else None
    ),
    "region_name": "us-east-1",
    "service_name": "dynamodb",
    "use_ssl": False,
    "verify": False,
}
