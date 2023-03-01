# pylint: skip-file
import ldap
import os


def unsafe_ldap() -> None:
    server = ldap.initialize("ldap://example:1389")
    # Noncompliant: No password, or stored directly as plain text
    server.simple_bind("cn=root")
    server.simple_bind_s("cn=root")
    server.bind_s("cn=root", None)
    server.bind("cn=root", "1234")


def safe_ldap(password: str) -> None:
    connect = ldap.initialize("ldap://example:1389")
    # Compliant, undeterministic password is used to bind the connection
    connect.simple_bind("cn=root", os.environ.get("LDAP_PASSWORD"))
    connect.simple_bind_s("cn=root", password)
    connect.bind_s("cn=root", os.environ.get("LDAP_PASSWORD"))
    connect.bind("cn=root", os.environ.get("LDAP_PASSWORD"))
