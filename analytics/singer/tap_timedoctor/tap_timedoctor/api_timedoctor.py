"""
Time Doctor API wrapper
    The access_token must have admin privileges
"""

## python3 -m pylint (default configuration)
# Your code has been rated at 10.00/10

import time
import urllib.request

def current_timestamp(offset=0.0):
    """ returns the current time stamp """
    return time.time() + offset

class Worker():
    """ class to represent a worker who make request to the API without exceeding the rate limit """

    def __init__(self, access_token):
        """ constructor """
        self.access_token = access_token
        self.url = "https://webapi.timedoctor.com"

        self.min_sslr = 0.75
        self.last_request_timestamp = current_timestamp()

    def sslr(self):
        """ seconds since last request """
        return current_timestamp() - self.last_request_timestamp

    def wait(self):
        """ wait until we can make another request to the API """
        time.sleep(max(self.min_sslr - self.sslr(), 0.0))
        self.last_request_timestamp = current_timestamp()

    def request(self, resource):
        """ Makes a request to the API """
        response = None
        status_code = None

        self.wait()

        try:
            headers = {}
            headers["Authorization"] = "Bearer " + self.access_token
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
        """ return the account info of the access_token owner """
        resource = self.url + "/v1.1/companies"
        return self.request(resource)

    def get_users(self, company_id):
        """ return a collection of user(s) under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/users"
        return self.request(resource)

    def get_worklogs(self, company_id, limit, offset):
        """ return a collection of users worklogs under the given company id """
        resource = self.url + "/v1.1/companies/" + company_id + "/worklogs"

        # fetch historical
        resource += "?start_date=2017-01-01&end_date=2999-12-31"
        resource += "&limit=" + str(limit) + "&offset=" + str(offset)

        # fetch working time, not breaks
        resource += "&breaks_only=0"

        # don't consolidate records to make information richer
        resource += "&consolidated=0"

        return self.request(resource)

    def get_computer_activity(self, company_id, user_id):
        """ returns screenshots, keystrokes, mouse activities for the specified user_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/screenshots"
        resource += "?start_date=2017-01-01&end_date=2999-12-31"
        resource += "&user_id=" + user_id
        return self.request(resource)

    # the next four functions:
    #   - were not tested/implemented due to service availability (v.g. poortime)
    #   - contribute negligible entropy to our use case (v.g. we don't have payrolls/webandapp)

    def get_poortime(self, company_id, limit, offset):
        """ return a collection of poortime usage under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/poortime"
        resource += "?start_date=1900-01-01&end_date=2999-12-31"
        resource += "&limit=" + limit + "&offset=" + offset
        return self.request(resource)

    def get_absent_and_late(self, company_id):
        """ return a collection of absent and late reason under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/absent-and-late"
        return self.request(resource)

    def get_payrolls(self, company_id):
        """ return a collection of payrolls under the given company Id """
        resource = self.url + "/v1.1/companies/" + company_id + "/payrolls"
        return self.request(resource)

    def get_webandapp(self, company_id):
        """ return a collection of web and apps used under the specified userID & date range """
        resource = self.url + "/v1.1/companies/" + company_id + "/webandapp"
        return self.request(resource)

    # the next five functions are automatically included in get_worklogs()

    def get_projects(self, company_id, user_id):
        """ return a collection of poortime usage under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/users/" + user_id + "/projects"
        resource += "/?all=1"
        return self.request(resource)

    def get_project_by_id(self, company_id, user_id, project_id):
        """ return a collection of poortime usage under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/users/" + user_id
        resource += "/projects/" + project_id
        return self.request(resource)

    def get_tasks(self, company_id, user_id):
        """ return a collection of poortime usage under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/users/" + user_id + "/tasks"
        return self.request(resource)

    def get_tasks_by_id(self, company_id, user_id, task_id):
        """ return a collection of poortime usage under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/users/" + user_id
        resource += "/tasks/" + task_id
        return self.request(resource)

    def get_users_by_id(self, company_id, user_id):
        """ return general info about a specific user under the given company_id """
        resource = self.url + "/v1.1/companies/" + company_id + "/users/" + user_id + ""
        return self.request(resource)
