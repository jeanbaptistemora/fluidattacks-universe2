# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# -*- coding: utf-8 -*-

"""Software Composition Analysis helper."""


import aiohttp
from fluidasserts import (
    CLOSED,
    OPEN,
    Unit,
    UNKNOWN,
)
from fluidasserts.helper import (
    asynchronous,
    lang,
)
from fluidasserts.utils.generic import (
    get_sha256,
)
from functools import (
    reduce,
)
import os
from pyparsing import (
    Regex,
)
import re
from typing import (
    Tuple,
)
import urllib.parse


def _build_cpe_url(
    product: str,
    version: str,
    keywords: Tuple[str, ...] = tuple(),
    target_software: str = str(),
) -> str:
    """Return a valid NVD CPE version 2.3 URI for the given parameters."""
    # https://nvd.nist.gov/products/cpe
    cpe_params: dict = dict(
        cpe="cpe",
        cpe_version="2.3",
        part="*",
        vendor="*",
        product=product or "__no_product__",
        version=version or "*",
        update="*",
        edition="*",
        language="*",
        software_edition="*",
        target_software=target_software or "*",
        target_hardware="*",
        other="*",
    )

    cpe_uri: str = ":".join(cpe_params.values()).rstrip(":*")

    cpe_product: str = _url_encode(cpe_uri)

    cpe_url: str = (
        "https://nvd.nist.gov/vuln/search/results"
        + f"?cpe_product={cpe_product}"
        + f"&form_type=Advanced"
        + f"&results_type=overview"
        + f"&search_type=all"
    )
    if keywords:
        keywords_query = " ".join(keywords)
        cpe_url += f"&query={_url_encode(keywords_query)}"

    return cpe_url


def _url_encode(string: str) -> str:
    """Return a url encoded string."""
    return urllib.parse.quote(string, safe="")


def _get_vuln_line(path: str, pkg: str, ver: str) -> int:
    """Return the line of first occurrence of pkg and version in path or 0."""
    if path is None:
        # There is no file to test
        return 0

    pkg = re.escape(pkg)
    if ver is None:
        regexes = [
            rf'"{pkg}"',
            rf"{pkg}",
        ]
    else:
        ver = re.escape(ver)
        regexes = [
            rf'"{pkg}".*?{ver}',
            rf"{pkg}.*?{ver}",
            rf"{ver}.*?{pkg}",
        ]

    for regex in regexes:
        grammar = Regex(regex, flags=re.MULTILINE | re.DOTALL)

        matches, _ = lang.parse_single(grammar, path)
        if matches:
            return matches[0].specific[0]

    # We were unable to find the package (and version) on that file
    return 0


# pylint: disable=unused-argument
@asynchronous.http_retry
async def get_vulns_vulndb_async(
    package_manager: str,
    path: str,
    package: str,
    version: str,
    retry: bool = True,
) -> tuple:
    """
    Search vulnerabilities on given package_manager/package/version.

    :param package_manager: Package manager.
    :param package: Package name.
    :param version: Package version.
    """
    config: dict = {
        "npm": {
            "keywords": ["node"],
            "target_software": "node.js",
        }
    }.get(package_manager, {})

    url = _build_cpe_url(package, version, **config)

    timeout = aiohttp.ClientTimeout(total=30.0)
    async with aiohttp.ClientSession(
        trust_env=True, timeout=timeout
    ) as session:
        async with session.get(url) as response:
            text = await response.text()

    vuln_titles = tuple()
    regex_total = re.compile(r'"vuln-matching-records-count">([0-9]+)')
    total = int(regex_total.findall(text)[0])
    regex_item = re.compile(r'vuln-detail-link-[0-9]+">(CVE-[0-9-]+)</a>')
    items = regex_item.findall(text)
    regex_name = re.compile(r'vuln-summary-[0-9]+">([^<]*?)</p>')
    names = regex_name.findall(text)

    if total > 0:
        vuln_titles = dict(zip(items, names))
        vuln_titles = tuple(
            reduce(
                lambda l, x: l.append(x) or l if x not in l else l,
                vuln_titles,
                [],
            )
        )

    return path, package, version, vuln_titles


def process_requirements(
    pkg_mgr: str, path: str, reqs: set, retry: bool = True
) -> tuple:
    """Return a dict mapping path to dependencies, versions and vulns."""
    if path and not os.path.exists(path):
        return UNKNOWN, "File does not exist"
    if not reqs:
        return CLOSED, "No packages have been found in that path"

    results = asynchronous.run_func(
        get_vulns_vulndb_async,
        [
            ((pkg_mgr, _path, dep, ver), {"retry": retry})
            for _path, dep, ver in reqs
        ],
    )
    results = list(filter(lambda x: isinstance(x, tuple), results))

    has_vulns, proj_vulns = None, {}
    for _path, dep, ver, vulns in results:
        if vulns:
            has_vulns = True
            component = (dep, ver)
            try:
                proj_vulns[_path].update({component: vulns})
            except KeyError:
                proj_vulns[_path] = {component: vulns}
    vulns = [
        Unit(
            where=f'{_path} [{pkg}@{ver if ver else "unpinned"}]',
            source="Lines",
            specific=[_get_vuln_line(_path, pkg, ver)],
            fingerprint={
                "sha256": get_sha256(_path),
                "associated_CVEs": deps[(pkg, ver)],
            },
        )
        for _path, deps in proj_vulns.items()
        for pkg, ver in deps
    ]

    if has_vulns:
        return OPEN, "Project has dependencies with vulnerabilities", vulns
    return CLOSED, "Project has dependencies with vulnerabilities"
