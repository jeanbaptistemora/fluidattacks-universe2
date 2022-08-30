"""TimeDoctor API wrapper."""

import datetime
import functools
import sys
from tap_timedoctor import (
    logs,
)
import time
from typing import (
    Any,
    Callable,
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


def retry_on_errors(func: Callable) -> Callable:
    """Decorate function to retry if an error is raised."""

    @functools.wraps(func)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        """Retry the function if status code is not 200."""
        for _ in range(10):
            (status_code, response) = func(*args, **kwargs)
            if status_code != 200:
                print("INFO: Retrying due to API error...")
                time.sleep(5.0)
            else:
                break
        return (status_code, response)

    return decorated


class Worker:
    """Class to represent a worker who make request to the API.

    It takes care of making the requests without exceeding the rate limit.
    """

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self.url = "https://api2.timedoctor.com"

        self.min_sslr = 0.75
        self.last_request_timestamp = current_timestamp()

    def sslr(self) -> float:
        """Number of seconds since last request."""
        return current_timestamp() - self.last_request_timestamp

    def wait(self) -> None:
        """Wait until we can make another request to the API."""
        time.sleep(max(self.min_sslr - self.sslr(), 0.0))
        self.last_request_timestamp = current_timestamp()

    @retry_on_errors
    def request(self, resource: str) -> StatusAndResponse:
        """Make a request to the API."""
        response = None
        status_code = 0

        self.wait()

        try:
            headers = {"Authorization": f"JWT {self.access_token}"}

            request = urllib.request.Request(resource, headers=headers)
            with urllib.request.urlopen(request) as result:
                response = result.read().decode("utf-8")
            status_code = 200
        except urllib.error.HTTPError as error:
            status_code = error.code
            if status_code == 401:
                print("INFO: Invalid token or credentials")
                sys.exit(1)
            elif status_code == 403:
                print("INFO: Unauthorized/Forbidden")
                sys.exit(1)
        except urllib.error.URLError as error:
            logs.log_error(f"URL:  [{request.full_url}] | {error}")

        return (status_code, response)

    def get_companies(self) -> StatusAndResponse:
        """Return the account info of the access_token owner."""
        resource = f"{self.url}/api/1.0/authorization"
        return self.request(resource)

    def get_users(
        self,
        company_id: str,
    ) -> StatusAndResponse:
        """Return a collection of user(s) under the given company_id."""
        resource = f"{self.url}/api/1.0/users?company={company_id}"
        return self.request(resource)

    def get_projects(
        self,
        company_id: str,
    ) -> StatusAndResponse:
        """Return a collection of projects info under the given company_id."""
        resource = f"{self.url}/api/1.0/projects?company={company_id}"
        return self.request(resource)

    def get_worklogs(
        self,
        company_id: str,
        user_id: str,
        options: Options,
    ) -> StatusAndResponse:
        """Return a collection of worklogs for a user id."""
        today = datetime.date.today()
        start_date = (
            options.start_date or today.replace(today.year - 1).isoformat()
        )
        end_date = options.end_date or today.isoformat()

        resource = (
            f"{self.url}/api/1.0/activity/worklog"
            f"?company={company_id}&user={user_id}"
            f"&detail=true&task-project-names=true"
            # fetch historical
            f"&from={start_date}&to={end_date}"
        )

        return self.request(resource)

    def get_computer_activity(
        self,
        company_id: str,
        user_id: str,
        offset: int,
        options: Options,
    ) -> StatusAndResponse:
        """Return screenshots, keystrokes, mouse activities for a user_id."""
        today = datetime.date.today()
        start_date = (
            options.start_date or today.replace(today.year - 1).isoformat()
        )
        end_date = options.end_date or today.isoformat()
        resource = (
            f"{self.url}/api/1.0/files/screenshot"
            f"?company={company_id}"
            f"&from={start_date}&to={end_date}"
            f"&user={user_id}"
            f"&limit={options.limit}&page={offset}"
        )
        return self.request(resource)

    def logout(self) -> StatusAndResponse:
        """Invalidate the token being currently used."""
        resource = "https://api2.timedoctor.com/api/1.0/logout"

        return self.request(resource)
