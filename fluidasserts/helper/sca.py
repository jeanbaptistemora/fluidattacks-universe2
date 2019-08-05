# -*- coding: utf-8 -*-

"""Software Composition Analysis helper."""

# standard imports
import os
import json
import aiohttp
import urllib.parse

# 3rd party imports
from functools import reduce


# local imports
from fluidasserts import Unit
from fluidasserts import OPEN, CLOSED, UNKNOWN
from fluidasserts.helper import asynchronous
from fluidasserts.utils.generic import get_sha256


def _url_encode(string: str) -> str:
    """Return a url encoded string."""
    return urllib.parse.quote(string, safe='')


@asynchronous.http_retry
async def get_vulns_ossindex_async(package_manager: str, path: str,
                                   package: str, version: str,
                                   retry: bool) -> tuple:
    """
    Search vulnerabilities on given package_manager/package/version.

    :param package_manager: Package manager.
    :param package: Package name.
    :param version: Package version.
    """
    if version:
        url = 'https://ossindex.net/v2.0/package/{}/{}/{}'.format(
            _url_encode(package_manager),
            _url_encode(package),
            _url_encode(version))
    else:
        url = 'https://ossindex.net/v2.0/package/{}/{}'.format(
            _url_encode(package_manager),
            _url_encode(package))

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as response:
            text = await response.text()

    vuln_titles = tuple()
    resp = json.loads(text)[0]
    if resp['id'] != 0 and resp['vulnerability-matches'] > 0:
        vulns = resp['vulnerabilities']
        vuln_titles = tuple({x['title']: ", ".join(x['versions'])}
                            for x in vulns)
        vuln_titles = tuple(reduce(
            lambda l, x: l.append(x) or l if x not in l else l,
            vuln_titles, []))
    return path, package, version, vuln_titles


def process_requirements(pkg_mgr: str, path: str,
                         reqs: set, retry: bool = True) -> tuple:
    """Return a dict mapping path to dependencies, versions and vulns."""
    if path and not os.path.exists(path):
        return UNKNOWN, 'File does not exist'
    if not reqs:
        return CLOSED, 'No packages have been found in that path'

    results = asynchronous.run_func(
        get_vulns_ossindex_async,
        [((pkg_mgr, _path, dep, ver, retry), {}) for _path, dep, ver in reqs])
    results = filter(lambda x: isinstance(x, tuple), results)

    has_vulns, proj_vulns = None, {}
    for _path, dep, ver, vulns in results:
        if vulns:
            has_vulns = True
            component = f'{dep}@{ver}' if ver else f'{dep}@unpinned'
            try:
                proj_vulns[_path].update({component: vulns})
            except KeyError:
                proj_vulns[_path] = {component: vulns}

    vulns = [Unit(where=_path,
                  attribute='dependencies',
                  specific=list(deps),
                  fingerprint={
                      'sha256': get_sha256(_path),
                      'vulnerabilities': deps,
                  })
             for _path, deps in proj_vulns.items()]

    if has_vulns:
        return OPEN, 'Project has dependencies with vulnerabilities', vulns
    return CLOSED, 'Project has dependencies with vulnerabilities'
