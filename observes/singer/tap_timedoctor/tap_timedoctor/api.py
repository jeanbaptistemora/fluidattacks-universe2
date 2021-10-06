"""TimeDoctor API wrapper."""

import datetime
import sys
from tap_timedoctor import (
    logs,
)
import time
from typing import (
    Any,
    NamedTuple,
    Optional,
    Tuple,
)
import urllib.error
import urllib.request


def current_timestamp(offset: float = 0.0) -> float:
    """Return the current timestamp."""
    return time.time() + offset


StatusAndResponse = Tuple[int, Any]


class Options(NamedTuple):
    limit: int
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Worker:
    """Class to represent a worker who make request to the API.

    It takes care of making the requests without exceeding the rate limit.
    """

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self.url = "https://webapi.timedoctor.com"

        self.min_sslr = 0.75
        self.last_request_timestamp = current_timestamp()

    def sslr(self) -> float:
        """Number of seconds since last request."""
        return current_timestamp() - self.last_request_timestamp

    def wait(self) -> None:
        """Wait until we can make another request to the API."""
        time.sleep(max(self.min_sslr - self.sslr(), 0.0))
        self.last_request_timestamp = current_timestamp()

    def request(self, resource: str) -> StatusAndResponse:
        """Make a request to the API."""
        response = None
        status_code = 0

        self.wait()

        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}

            request = urllib.request.Request(resource, headers=headers)
            with urllib.request.urlopen(request) as result:
                response = result.read().decode("utf-8")
            status_code = 200
        except urllib.error.HTTPError as error:
            status_code = error.code
            if status_code == 401:
                print("INFO: Please reauthorize using the refresh token")
                sys.exit(1)
            elif status_code == 403:
                print("INFO: Unauthorized/Forbidden")
                sys.exit(1)
        except urllib.error.URLError as error:
            logs.log_error(f"URL:  [{request.full_url}] | {error}")

        return (status_code, response)

    def get_companies(self) -> StatusAndResponse:
        """Return the account info of the access_token owner."""
        resource = f"{self.url}/v1.1/companies"
        return self.request(resource)

    def get_users(self, company_id: str) -> StatusAndResponse:
        """Return a collection of user(s) under the given company_id."""
        resource = f"{self.url}/v1.1/companies/{company_id}/users"
        return self.request(resource)

    def get_worklogs(
        self,
        company_id: str,
        offset: int,
        options: Options,
    ) -> StatusAndResponse:
        """Return a collection of users worklogs under the given company id."""
        today = datetime.date.today()
        start_date = (
            options.start_date or today.replace(today.year - 1).isoformat()
        )
        end_date = options.end_date or today.isoformat()

        resource = (
            f"{self.url}/v1.1/companies/{company_id}/worklogs"
            # fetch historical
            f"?start_date={start_date}&end_date={end_date}"
            f"&limit={options.limit}&offset={offset}"
            # fetch working time, not breaks
            f"&breaks_only=0"
            # don't consolidate records to make information richer
            f"&consolidated=0"
        )

        return self.request(resource)

    def get_computer_activity(
        self,
        company_id: str,
        user_id: str,
        options: Options,
    ) -> StatusAndResponse:
        """Return screenshots, keystrokes, mouse activities for a user_id."""
        today = datetime.date.today()
        start_date = (
            options.start_date or today.replace(today.year - 1).isoformat()
        )
        end_date = options.end_date or today.isoformat()
        resource = (
            f"{self.url}/v1.1/companies/{company_id}/screenshots"
            f"?start_date={start_date}&end_date={end_date}"
            f"&user_id={user_id}"
            f"&limit=0&screenshots_limit={options.limit}&offset=0"
        )
        return self.request(resource)
