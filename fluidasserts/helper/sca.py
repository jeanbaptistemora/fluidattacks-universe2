# -*- coding: utf-8 -*-

"""Software Composition Analysis helper."""

# standard imports
import json
import aiohttp
import urllib.parse

# 3rd party imports
from functools import reduce


# local imports
from fluidasserts import show_close
from fluidasserts import show_open
from fluidasserts import show_unknown
from fluidasserts.helper import http
from fluidasserts.helper import asynchronous


def _url_encode(string: str) -> str:
    """Return a url encoded string."""
    return urllib.parse.quote(string, safe='')


@http.retry
def get_vulns_ossindex(package_manager: str, package: str,
                       version: str, retry: bool) -> tuple:
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

    sess = http.HTTPSession(url)
    resp = json.loads(sess.response.text)[0]
    vuln_titles = tuple()
    if resp['id'] == 0:
        return vuln_titles
    if int(resp['vulnerability-matches']) > 0:
        vulns = resp['vulnerabilities']
        vuln_titles = tuple([x['title'], ", ".join(x['versions'])]
                            for x in vulns)
        vuln_titles = tuple(reduce(
            lambda l, x: l.append(x) or l if x not in l else l,
            vuln_titles, []))
    return vuln_titles


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
        vuln_titles = tuple([x['title'], ", ".join(x['versions'])]
                            for x in vulns)
        vuln_titles = tuple(reduce(
            lambda l, x: l.append(x) or l if x not in l else l,
            vuln_titles, []))
    return path, package, version, vuln_titles


def process_requirement(pkg_mgr: str, package: str, version: str = None,
                        retry: bool = True) -> bool:
    """
    Search vulnerabilities on given package/version.

    :param package: Package name.
    :param version: Package version.
    """
    try:
        vulns = get_vulns_ossindex(pkg_mgr, package, version, retry)
    except http.ConnError as exc:
        show_unknown('Could not connect to SCA provider',
                     details=dict(error=str(exc).replace(':', ',')))
        return False
    if vulns:
        show_open('Software has vulnerabilities',
                  details=dict(package=package, version=version,
                               vuln_num=len(vulns), vulns=vulns))
        return True
    show_close('Software does not have vulnerabilities',
               details=dict(package=package, version=version))
    return False


def process_requirements(pkg_mgr: str, path: str,
                         reqs: set, retry: bool = True) -> tuple:
    """Return a dict mapping path to dependencies, versions and vulns."""
    if not reqs:
        show_unknown('Not packages found in project',
                     details=dict(path=path))
        return False

    results = asynchronous.run_func(
        get_vulns_ossindex_async,
        [((pkg_mgr, path, dep, ver, retry), {}) for path, dep, ver in reqs])
    results = filter(lambda x: isinstance(x, tuple), results)

    has_vulns, proj_vulns = None, {}
    for path, dep, ver, vulns in results:
        if vulns:
            has_vulns = True
            try:
                proj_vulns[path][f'{dep} {ver}'] = vulns
            except KeyError:
                proj_vulns[path] = {f'{dep} {ver}': vulns}

    if has_vulns:
        show_open('Project has dependencies with vulnerabilities',
                  details=dict(project_path=path,
                               vulnerabilities=proj_vulns))
        return True

    show_close('Project has not dependencies with vulnerabilities',
               details=dict(project_path=path))
    return False
