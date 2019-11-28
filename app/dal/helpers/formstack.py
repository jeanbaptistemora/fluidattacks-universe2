# -*- coding: utf-8 -*-
"""Functions to consume the Formstack API."""

import json
import random
import requests

from django.views.decorators.cache import cache_control
from retrying import retry
import rollbar

from app.dto import remission
from __init__ import FI_FORMSTACK_TOKENS


requests.adapters.DEFAULT_RETRIES = 10


class FormstackAPI():
    """Class to consume the Formstack API."""

    headers_config = {}
    SUBMISSION_URL = "https://www.formstack.com/api/v2/submission/:id.json"

    def __init__(self):
        """ Constructor. """
        self.headers_config['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) FLUIDIntegrates/1.0'
        self.token_list = FI_FORMSTACK_TOKENS.split(',')
        self.failed_attemps = 0
        self.current_token = self.token_list[random.randint(
            0, len(self.token_list) - 1)]

    def requests_per_page(self, method, url, data=None):
        """Return the request from Formstack."""
        formstack_response = self.request(method, url, data)
        total_submissions = int(formstack_response["total"])
        while total_submissions > data['per_page']:
            data["page"] += 1
            next_page_submissions = self.request(
                method,
                url,
                data)
            formstack_response["submissions"].extend(
                next_page_submissions["submissions"])
            total_submissions -= data['per_page']
        return formstack_response

    def request(self, method, url, data=None):
        """Validate if a token is available."""
        formstack_request = self.execute_request(method, url, data)
        while formstack_request.status_code == 429:
            self.failed_attemps += 1
            if self.failed_attemps > 9:
                message = 'Warning: Integrates is running out of Formstack API tokens. \
                    9 failed requests in a row'
                rollbar.report_message(message, 'warning')
                break
            else:
                self.refresh_token()
                formstack_request = self.execute_request(method, url, data)
        return json.loads(formstack_request.text)

    @retry(retry_on_exception=ConnectionError, stop_max_attempt_number=5)
    def execute_request(self, method, url, data=None):
        """ Build the requests used to consult in Formstack. """
        executed_request = None
        try:
            self.headers_config['Authorization'] = 'Bearer {}'.format(
                self.current_token)
            if method != "GET":
                self.headers_config["cache-control"] = "no-cache"
                self.headers_config["content-type"] = \
                    "application/x-www-form-urlencoded"
                executed_request = requests.request(
                    method, url, data=data, headers=self.headers_config)
            else:
                self.headers_config['content-type'] = 'application/json'
                params = '&'.join(['{}={}'.format(k, v)
                                   for k, v in list(data.items())]) if data else ''
                executed_request = requests.request(
                    method, url='{}?{}'.format(url, params),
                    headers=self.headers_config)
        # Formstack SSLError
        except requests.exceptions.SSLError:
            executed_request = None
        # Formstack Connection timeout
        except requests.exceptions.Timeout:
            executed_request = None
        # Fail token
        except requests.exceptions.HTTPError:
            executed_request = None
        # Fail connection
        except ConnectionError:
            executed_request = None
        # Fail json format
        except ValueError:
            executed_request = None
        # Fail json
        except TypeError:
            executed_request = None
        return executed_request

    def refresh_token(self):
        next_index = random.randint(0, len(self.token_list) - 1)
        self.current_token = self.token_list[next_index]

    @cache_control(max_age=600)
    def get_submission(self, submission_id):
        """ Get a submission by ID. """
        url = self.SUBMISSION_URL.replace(":id", submission_id)
        return self.request("GET", url)

    def get_remmisions(self, project):
        """ Get the remissions of a project by its name. """
        data = {'search_field_1': remission.PROJECT_FIELD_ID,
                'search_value_1': project,
                'page': 1,
                'per_page': 50}
        return self.requests_per_page("GET", remission.URL, data=data)
