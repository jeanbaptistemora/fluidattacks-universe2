#!/usr/bin/env python3

"""Gitlab API streamer."""

import os
import sys
import json
import time
import urllib.parse
import urllib.error
import urllib.request
from typing import Any


def log(*args, **kwargs):
    """Print to stderr."""
    kwargs['file'] = sys.stderr
    kwargs['flush'] = True
    print(*args, **kwargs)


class API():
    """Class to represent an API worker."""

    def __init__(self, token):
        self.token: str = token
        self.success: bool = None
        self.request: Any = None

        self.json = None
        self.response: Any = None
        self.res_headers: Any = None

    def get(self, resource) -> None:
        """Make a request to the API."""
        self.success, self.response = False, {}
        try:
            log(f'FETCH: {resource}')
            self.request = urllib.request.Request(
                url=f'https://gitlab.com/api/v4/{resource}',
                headers={'Private-Token': self.token})
            self.response = urllib.request.urlopen(self.request)
            self.json = json.loads(self.response.read().decode())
            self.res_headers = dict(self.response.info())
        except urllib.error.HTTPError as error:
            log(f'ERROR: urllib.error.HTTPError, {error}')
        except urllib.error.URLError as error:
            log(f'ERROR: urllib.error.URLError, {error}')
        except json.JSONDecodeError as error:
            log(f'ERROR: json.JSONDecodeError, {error}')
        else:
            self.success = True

    def paginate(self, resource, extra_query_args: str = ''):
        """Paginate a resource."""
        page: int = 1
        errors: int = 0
        while True:
            self.get(f'{resource}?page={page}{extra_query_args}')
            if self.success:
                page += 1
                errors = 0
                yield
            else:
                time.sleep(1.0)
                errors += 1
            if self.res_headers and not self.res_headers['X-Next-Page']:
                break
            if errors > 10:
                page += 1


def main():
    """Usual entrypoint."""
    try:
        token: str = os.environ['GITLAB_PASS']
    except KeyError:
        log(f'Please set GITLAB_PASS as an environment variable.')
    else:
        api = API(token)
        project = urllib.parse.quote(sys.argv[1], safe='')
        for _ in api.paginate(
                f'projects/{project}/merge_requests', '&scope=all'):
            for obj in api.json:
                print(json.dumps({'stream': 'merge_requests', 'record': obj}))
        for _ in api.paginate(f'projects/{project}/jobs'):
            for obj in api.json:
                print(json.dumps({'stream': 'jobs', 'record': obj}))


if __name__ == '__main__':
    main()
