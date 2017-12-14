# -*- coding: utf-8 -*-
"""Funciones para consumir la API de Formstack."""

import json
import requests
from requests.exceptions import ConnectionError
from retrying import retry
# pylint: disable=E0402

requests.adapters.DEFAULT_RETRIES = 10

class FrmAPI(object):

    headers_config = {}
    #TOKEN = "7f7599e833e78a4f8c0420fe89948491"
    TOKEN = 'e9ef81ddb47c0639014d09f8668bd4d1'
    SUBMISSION_URL = "https://www.formstack.com/api/v2/submission/:id.json"

    def __init__(self):
        """Constructor."""
        self.headers_config['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) FLUIDIntegrates/1.0'

    @retry(retry_on_exception=ConnectionError, stop_max_attempt_number=5)
    def request(self, method, url, data=None):
        """Construye las peticiones usadas para consultar Formstack."""
        executed_request = None
        try:
            if method != "GET":
                self.headers_config["cache-control"] = "no-cache"
                self.headers_config["content-type"] = \
                    "application/x-www-form-urlencoded"
                url += "?oauth_token=:token".replace(":token",
                                                     self.TOKEN)
            else:
                if not data:
                    data = {"oauth_token": self.TOKEN}
                else:
                    data["oauth_token"] = self.TOKEN
            formstack_request = requests.request(
                method, url,
                data=data, headers=self.headers_config
            )
            executed_request = json.loads(formstack_request.text)
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

    def update(self, request_id, data_dto):
        """Actualiza un hallazgo en formstack."""
        url = self.SUBMISSION_URL.replace(":id", request_id)
        return self.request("PUT", url, data=data_dto)
