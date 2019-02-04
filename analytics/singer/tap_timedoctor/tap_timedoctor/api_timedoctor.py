"""TimeDoctor API wrapper.
"""

import time
import urllib.error
import urllib.request


def current_timestamp(offset=0.0):
    """Returns the current timestamp.
    """

    return time.time() + offset


class Worker():
    """Class to represent a worker who make request to the API.

    It takes care of making the requests without exceeding the rate limit.
    """

    def __init__(self, access_token):
        self.access_token = access_token
        self.url = "https://webapi.timedoctor.com"

        self.min_sslr = 0.75
        self.last_request_timestamp = current_timestamp()

    def sslr(self):
        """Seconds since last request.
        """

        return current_timestamp() - self.last_request_timestamp

    def wait(self):
        """Wait until we can make another request to the API.
        """

        time.sleep(max(self.min_sslr - self.sslr(), 0.0))
        self.last_request_timestamp = current_timestamp()

    def request(self, resource):
        """Makes a request to the API.
        """

        response = None
        status_code = None

        self.wait()

        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            request = urllib.request.Request(resource, headers=headers)
            response = urllib.request.urlopen(request).read().decode('utf-8')
            status_code = 200
        except urllib.error.HTTPError as error:
            status_code = error.code
            if status_code == 401:
                print("INFO: Please reauthorize using the refresh token")
                exit(1)
            elif status_code == 403:
                print("INFO: Unauthorized/Forbidden")
                exit(1)
        except urllib.error.URLError:
            pass

        return (status_code, response)

    def get_companies(self):
        """Return the account info of the access_token owner.
        """

        resource = f"{self.url}/v1.1/companies"
        return self.request(resource)

    def get_users(self, company_id):
        """Return a collection of user(s) under the given company_id.
        """

        resource = f"{self.url}/v1.1/companies/{company_id}/users"
        return self.request(resource)

    def get_worklogs(self, company_id, limit, offset):
        """Return a collection of users worklogs under the given company id.
        """

        resource = (
            f"{self.url}/v1.1/companies/{company_id}/worklogs"

            # fetch historical
            f"?start_date=2019-01-01&end_date=2999-12-31"
            f"&limit={limit}&offset={offset}"

            # fetch working time, not breaks
            f"&breaks_only=0"

            # don't consolidate records to make information richer
            f"&consolidated=0"
        )

        return self.request(resource)

    def get_computer_activity(self, company_id, user_id):
        """Returns screenshots, keystrokes, mouse activities for a user_id.
        """

        resource = (
            f"{self.url}/v1.1/companies/{company_id}/screenshots"
            f"?start_date=2019-01-01&end_date=2999-12-31"
            f"&user_id={user_id}"
        )
        return self.request(resource)
