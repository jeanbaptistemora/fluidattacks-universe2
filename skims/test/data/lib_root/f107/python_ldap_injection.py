# pylint: skip-file
from flask import (
    request,
)
import ldap
import ldap.filter


def unsafe_ldap() -> None:
    dn = request.args["dn"]
    username = request.args["username"]

    search_filter = "(&(objectClass=*)(uid=" + username + "))"
    ldap_connection = ldap.initialize("ldap://127.0.0.1:389")
    # Noncompliant
    ldap_connection.search_s(dn, ldap.SCOPE_SUBTREE, search_filter)


def safe_ldap() -> None:
    # Escape distinguished names special characters
    dn = "dc=%s" % ldap.dn.escape_dn_chars(request.args["dc"])
    # Escape search filters special characters
    username = ldap.filter.escape_filter_chars(request.args["username"])

    search_filter = "(&(objectClass=*)(uid=" + username + "))"
    ldap_connection = ldap.initialize("ldap://127.0.0.1:389")
    # Compliant
    ldap_connection.search_s(dn, ldap.SCOPE_SUBTREE, search_filter)
