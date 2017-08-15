#/usr/bin/python

from fluidasserts.format import cookie
from fluidasserts.service import tcp
from fluidasserts.service import http
from fluidasserts.service import ssl


url = 'https://localhost:8000'
cookie.has_not_httponly_set('Integratesv3', url)
cookie.has_not_secure_set('Integratesv3', url)

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
http.has_dirlisting('https://localhost:8000/icons')
http.is_sessionid_exposed(url)
server = 'localhost'
http.is_version_visible(server, port=8000)

text = 'Login Azure'
http.has_not_text('https://localhost:8000', text)
