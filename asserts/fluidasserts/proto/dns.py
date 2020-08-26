# -*- coding: utf-8 -*-

"""This module allows to check vulnerabilities in DNS systems."""

# standard imports
from typing import Set, Tuple, List
from contextlib import suppress

# 3rd party imports
import socket
import dns.dnssec
import dns.query
import dns.rdatatype
import dns.resolver
import dns.update
from dns.zone import BadZone
from dns.zone import NoNS
from dns.zone import NoSOA
from dns.zone import from_xfr


# local imports
from fluidasserts import Unit, DAST, LOW, MEDIUM, HIGH, OPEN, CLOSED
from fluidasserts.utils.decorators import api, unknown_if


DOMAIN = str
NAMESERVER = str


def _get_resolver(nameserver: NAMESERVER) -> dns.resolver.Resolver:
    """Return a resolver configured to query the provided nameserver."""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [nameserver]
    return resolver


def _recursive_query_dns(
        domain: DOMAIN,
        nameserver: NAMESERVER,
        results: Set[Tuple[DOMAIN, DOMAIN]]) -> None:
    """Append tuples of (origin, target) to results."""
    answers = []

    # Canonicalize the original domain
    domain = dns.name.from_text(domain).to_text()

    # Instantiate a custom resolver set to query the provided nameserver
    resolver = _get_resolver(nameserver)

    # Query for the records
    for rdtype in (dns.rdatatype.A, dns.rdatatype.AAAA, dns.rdatatype.CNAME):
        with suppress(dns.resolver.NoAnswer):
            _answers = resolver.query(domain, rdtype=rdtype)
            answers.extend(_answers.rrset.items)

    results.update((domain, str(target)) for target in answers)


def _get_result_as_tuple(*,
                         nameserver: str, domain: str,
                         msg_open: str, msg_closed: str,
                         open_if: bool = None,
                         vulns: List[str] = None) -> tuple:
    """Return the tuple version of the Result object."""
    domain = domain.strip('.')

    units: List[Unit] = [
        Unit(where=nameserver,
             specific=vulns or [
                 f'{domain} {msg_open if open_if or vulns else msg_closed}'])]

    if open_if or vulns:
        return OPEN, msg_open, units, []
    return CLOSED, msg_closed, [], units


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error,
            dns.exception.Timeout,
            dns.exception.FormError,
            dns.resolver.NoNameservers,
            dns.resolver.NXDOMAIN)
def has_subdomain_takeover(
        domain: DOMAIN,
        nameserver: NAMESERVER,
        attacker_controlled_domains: List[DOMAIN]) -> tuple:
    """
    Check if DNS records point to an attacker controlled site.

    Check is done recursively starting from domain and all the A, AAAA, and
    CNAME records found down the road.

    See `Tutorial <https://www.hackerone.com/blog/Guide-Subdomain-Takeovers>`_.

    :param domain: IPv4, IPv6, or domain to test.
    :param attacker_controlled_domains: A list of domains to expect as
                                        vulnerable.
    :rtype: :class:`fluidasserts.Result`
    """
    origin_to_target: Set[Tuple[DOMAIN, DOMAIN]] = set()

    # Fill the results
    _recursive_query_dns(domain, nameserver, origin_to_target)

    vuln_records: List[DOMAIN] = list(
        f'Record: {origin} -> {target}'
        for origin, target in origin_to_target
        for controlled_domain in attacker_controlled_domains
        if controlled_domain in target)

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open=('is vulnerable to a sub-domain takeover because one of the '
                  'records point to a site that can be controlled by an '
                  'attacker'),
        msg_closed='is safe against a sub-domain takeover',
        vulns=vuln_records)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error, dns.exception.Timeout, dns.exception.FormError)
def is_xfr_enabled(domain: str, nameserver: str) -> tuple:
    """
    Check if zone transfer is enabled.

    :param domain: Name of the zone to transfer.
    :param nameserver: IPv4 or 6 to test.
    """
    is_zone_transfer_enabled: bool = False

    axfr_query = dns.query.xfr(nameserver, domain, timeout=5,
                               relativize=False, lifetime=10)

    with suppress(NoSOA, NoNS, BadZone, dns.query.BadResponse,
                  dns.query.TransferError):

        zone = from_xfr(axfr_query, relativize=False)

        if str(zone.origin).rstrip('.'):
            is_zone_transfer_enabled = True

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open='zone transfer is enabled on name server',
        msg_closed='zone transfer is disabled on name server',
        open_if=is_zone_transfer_enabled)


@api(risk=HIGH, kind=DAST)
@unknown_if(socket.error, dns.exception.Timeout)
def is_dynupdate_enabled(domain: str, nameserver: str) -> tuple:
    """
    Check if zone updating is enabled.

    :param domain: Name of the zone to transfer.
    :param nameserver: IPv4 or 6 to test.
    """
    is_zone_update_enabled: bool = False

    with suppress(dns.query.BadResponse):
        update = dns.update.Update(domain)
        update.add('newrecord', 3600, dns.rdatatype.A, '10.10.10.10')

        response = dns.query.tcp(update, nameserver, timeout=5)

        if response.rcode() <= 0:
            is_zone_update_enabled = True

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open='zone update is enabled on name server',
        msg_closed='zone update is disabled on name server',
        open_if=is_zone_update_enabled)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(dns.exception.Timeout,
            dns.exception.SyntaxError,
            dns.resolver.NoNameservers)
def has_cache_poison(domain: str, nameserver: str) -> tuple:
    """
    Check if cache poisoning is possible.

    The check is made by looking DNSSEC records.

    :param domain: Name of the zone to transfer.
    :param nameserver: IPv4 or 6 to test.
    """
    is_vulnerable: bool = False

    name = dns.name.from_text(domain)

    try:
        response = _get_resolver(nameserver).query(name, 'DNSKEY')
    except dns.resolver.NoAnswer:
        is_vulnerable = True
    else:
        if response.response.rcode() != 0 or len(response.rrset) != 2:
            is_vulnerable = True

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open='cache poisoning is possible on name server',
        msg_closed='cache poisoning is not possible on name server',
        open_if=is_vulnerable)


@api(risk=LOW, kind=DAST)
@unknown_if(socket.error, dns.exception.Timeout)
def has_cache_snooping(nameserver: str, domain: str = 'google.com.') -> tuple:
    """
    Check if nameserver has cache snooping.

    (supports non recursive queries)
    :param nameserver: IPv4 or 6 to test.
    """
    is_vulnerable: bool = False

    name = dns.name.from_text(domain)

    with suppress(dns.exception.SyntaxError):
        # Make a recursive request to fill out the cache
        request = dns.message.make_query(name,
                                         dns.rdatatype.A,
                                         dns.rdataclass.IN)

        dns.query.udp(request, nameserver, timeout=5)

        # Make a non-recursive request
        request = dns.message.make_query(name,
                                         dns.rdatatype.A,
                                         dns.rdataclass.IN)

        request.flags ^= dns.flags.RD

        response = dns.query.udp(request, nameserver, timeout=5)

        if response.rcode() == 0:
            is_vulnerable = True

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open='cache snooping is possible on name server',
        msg_closed='cache snooping is not possible on name server',
        open_if=is_vulnerable)


@api(risk=LOW, kind=DAST)
@unknown_if(socket.error, dns.exception.Timeout)
def has_recursion(nameserver: str, domain: str = 'google.com.') -> tuple:
    """
    Check if nameserver has recursion enabled.

    :param nameserver: IPv4 or 6 to test.
    """
    is_vulnerable: bool = False

    name = dns.name.from_text(domain)

    with suppress(dns.exception.SyntaxError):
        # Make a recursive request
        request = dns.message.make_query(name,
                                         dns.rdatatype.A,
                                         dns.rdataclass.IN)

        response = dns.query.udp(request, nameserver, timeout=5)

        if response.rcode() == 0:
            is_vulnerable = True

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open='recursion is possible on name server',
        msg_closed='recursion is not possible on name server',
        open_if=is_vulnerable)


@api(risk=MEDIUM, kind=DAST)
@unknown_if(socket.error, dns.exception.Timeout)
def can_amplify(nameserver: str, domain: str = 'google.com.') -> tuple:
    """
    Check if nameserver allows amplification attacks.

    :param nameserver: IPv4 or 6 to test.
    """
    is_vulnerable: bool = False

    name = dns.name.from_text(domain)

    with suppress(dns.exception.SyntaxError):
        # Make a recursive request
        request = dns.message.make_query(name,
                                         dns.rdatatype.A,
                                         dns.rdataclass.IN)

        response = dns.query.udp(request, nameserver, timeout=5)

        if response.rcode() == 0:
            request = dns.message.make_query(name, dns.rdatatype.ANY)
            request.flags |= dns.flags.AD
            request.find_rrset(request.additional, dns.name.root, 65535,
                               dns.rdatatype.OPT, create=True,
                               force_unique=True)
            request_len = len(request.to_text())

            response = dns.query.udp(request, nameserver, timeout=5)
            response_len = sum(len(x.to_text()) for x in response.answer)

            if response_len > request_len:
                is_vulnerable = True

    return _get_result_as_tuple(
        nameserver=nameserver, domain=domain,
        msg_open='amplification attack is possible on name server',
        msg_closed='amplification attack  is not possible on name server',
        open_if=is_vulnerable)
