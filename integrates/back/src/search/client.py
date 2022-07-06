from botocore.credentials import (
    Credentials,
)
from context import (
    FI_AWS_ACCESS_KEY_ID,
    FI_AWS_OPENSEARCH_HOST,
    FI_AWS_REGION_NAME,
    FI_AWS_SECRET_ACCESS_KEY,
    FI_AWS_SESSION_TOKEN,
)
from opensearchpy import (
    AsyncOpenSearch,
    AWSV4SignerAuth,
)

AUTH = AWSV4SignerAuth(
    Credentials(
        FI_AWS_ACCESS_KEY_ID,
        FI_AWS_SECRET_ACCESS_KEY,
        FI_AWS_SESSION_TOKEN,
    ),
    FI_AWS_REGION_NAME,
)

CLIENT = AsyncOpenSearch(
    hosts=[FI_AWS_OPENSEARCH_HOST],
    http_auth=AUTH,
    use_ssl=True,
    verify_certs=True,
    http_compress=True,
)
