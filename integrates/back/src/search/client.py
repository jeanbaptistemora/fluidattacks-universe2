from boto3 import (
    Session,
)
from botocore.auth import (
    SigV4Auth,
)
from botocore.awsrequest import (
    AWSRequest,
)
from botocore.credentials import (
    Credentials,
)
from context import (
    FI_AWS_OPENSEARCH_HOST,
    FI_AWS_REGION_NAME,
    FI_ENVIRONMENT,
)
from contextlib import (
    AsyncExitStack,
)
from opensearchpy import (
    AIOHttpConnection,
    AsyncOpenSearch,
)
from opensearchpy.helpers.signer import (
    OPENSEARCH_SERVICE,
)
from typing import (
    Any,
    Optional,
)
from urllib.parse import (
    urlencode,
)


class AsyncAWSConnection(AIOHttpConnection):
    """
    Extend base async connection to support AWS credentials

    Pending contribution to upstream
    https://github.com/opensearch-project/opensearch-py/issues/131
    """

    def __init__(
        self, aws_credentials: Credentials, aws_region: str, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.aws_credentials = aws_credentials
        self.aws_region = aws_region
        self.signer = SigV4Auth(
            self.aws_credentials,
            OPENSEARCH_SERVICE,
            self.aws_region,
        )

    async def perform_request(  # pylint: disable=too-many-arguments
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        body: Optional[bytes] = None,
        timeout: Optional[float] = None,
        ignore: tuple[int, ...] = (),
        headers: Optional[dict[str, str]] = None,
    ) -> tuple[int, dict[str, str], str]:
        headers_ = headers if headers else {}
        query_string = "?" + urlencode(params) if params else ""
        aws_request = AWSRequest(
            data=body,
            headers=headers_,
            method=method.upper(),
            url="".join([self.url_prefix, self.host, url, query_string]),
        )

        self.signer.add_auth(aws_request)
        signed_headers = dict(aws_request.headers.items())
        all_headers = {**headers_, **signed_headers}

        return await super().perform_request(
            method, url, params, body, timeout, ignore, all_headers
        )


SESSION = Session()
CLIENT_OPTIONS = {
    "aws_credentials": SESSION.get_credentials(),
    "aws_region": FI_AWS_REGION_NAME,
    "connection_class": AsyncAWSConnection,
    "hosts": [FI_AWS_OPENSEARCH_HOST],
    "http_compress": False,
    "use_ssl": FI_ENVIRONMENT == "production",
    "verify_certs": FI_ENVIRONMENT == "production",
}
CONTEXT_STACK = None
CLIENT = None


async def search_startup() -> None:
    # pylint: disable=global-statement
    global CONTEXT_STACK, CLIENT

    CONTEXT_STACK = AsyncExitStack()
    CLIENT = await CONTEXT_STACK.enter_async_context(
        AsyncOpenSearch(**CLIENT_OPTIONS)
    )


async def search_shutdown() -> None:
    if CONTEXT_STACK:
        await CONTEXT_STACK.aclose()


async def get_client() -> AsyncOpenSearch:
    if CLIENT is None:
        await search_startup()

    return CLIENT
