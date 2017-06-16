#/usr/bin/python

from fluidasserts.system import linux_generic
from fluidasserts.system import windows_server_2008_plus
from fluidasserts.format import string
from fluidasserts.format import cookie
from fluidasserts.format import html
from fluidasserts.format import pdf
from fluidasserts.service import smtp
from fluidasserts.service import dns
from fluidasserts.service import tcp
from fluidasserts.service import http
from fluidasserts.service import ssl
from fluidasserts.service import ldap
from fluidasserts.service import ftp


url = 'https://localhost:8000'
cookie.has_not_http_only(url, 'Integratesv3')
cookie.has_not_secure(url, 'Integratesv3')

server = 'localhost'
tcp.is_port_open(server, port=3389)

site = 'localhost'
port = 8000
ssl.is_cert_cn_not_equal_to_site(site, port)
ssl.is_cert_inactive(site, port)
ssl.is_cert_validity_lifespan_unsafe(site, port)
ssl.is_pfs_disabled(site, port)
ssl.is_sslv3_enabled(site, port)
ssl.is_tlsv1_enabled(site, port)

url = 'https://localhost:8000'
http.is_header_x_asp_net_version_missing(url)
http.is_header_access_control_allow_origin_missing(url)
http.is_header_cache_control_missing(url)
http.is_header_content_security_policy_missing(url)
http.is_header_content_type_missing(url)
http.is_header_expires_missing(url)
http.is_header_pragma_missing(url)
http.is_header_server_insecure(url)
http.is_header_x_content_type_options_missing(url)
http.is_header_x_frame_options_missing(url)
http.is_header_perm_cross_dom_pol_missing(url)
http.is_header_x_xxs_protection_missing(url)
http.is_header_hsts_missing(url)
http.is_basic_auth_enabled(url)
http.has_trace_method(url)
http.has_delete_method(url)
http.has_put_method(url)
http.has_dirlisting('https://localhost/icons')
http.is_sessionid_exposed(url)
server = 'localhost'
http.is_version_visible(server, port=8000)

text = 'Log in with Google'
http.has_not_text('https://localhost:8000', text)

http.is_not_https_required('http://localhost:8000')
