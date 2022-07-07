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
    FI_AWS_ACCESS_KEY_ID,
    FI_AWS_OPENSEARCH_HOST,
    FI_AWS_REGION_NAME,
    FI_AWS_SECRET_ACCESS_KEY,
    FI_AWS_SESSION_TOKEN,
)
from opensearchpy import (
    AIOHttpConnection,
    AsyncOpenSearch,
)
from opensearchpy.helpers.signer import (
    OPENSEARCH_SERVICE,
)
from safe_pickle import (
    Any,
)
from typing import (
    Optional,
)


class AsyncAWSConnection(AIOHttpConnection):
    """
    Extend base async connection to support AWS credentials

    https://github.com/opensearch-project/opensearch-py/issues/131
    """

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
        aws_request = AWSRequest(
            data=body,
            headers=headers_,
            method=method.upper(),
            url="".join([self.url_prefix, self.host, url]),
        )
        signer = SigV4Auth(
            Credentials(
                FI_AWS_ACCESS_KEY_ID,
                FI_AWS_SECRET_ACCESS_KEY,
                FI_AWS_SESSION_TOKEN,
            ),
            OPENSEARCH_SERVICE,
            FI_AWS_REGION_NAME,
        )
        signer.add_auth(aws_request)
        signed_headers = dict(aws_request.headers.items())
        all_headers = {**headers_, **signed_headers}

        return await super().perform_request(
            method, url, params, body, timeout, ignore, all_headers
        )


CLIENT = AsyncOpenSearch(
    connection_class=AsyncAWSConnection,
    hosts=[FI_AWS_OPENSEARCH_HOST],
    port=443,
    use_ssl=True,
    verify_certs=True,
)
