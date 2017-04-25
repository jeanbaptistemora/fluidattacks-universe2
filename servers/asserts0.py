# -*- coding: utf-8 -*-

from fluidasserts.service import http
from fluidasserts.service import ssl
# from fluidasserts.service import dns

url = 'https://fluid.la'
text = 'in customers and users of the applications'
http.generic_http_assert('https://fluid.la', text)
text = 'Blog de FLUID | Expertos en Ethical Hacking - Pentesting'
http.generic_http_assert('https://fluid.la/blog', text)
text = 'Sus datos han sido registrados y pronto nos comunicaremos con usted.'
http.generic_http_assert('https://fluid.la/es/servicios/confirmacion/', text)
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
http.is_sessionid_exposed(url)

server = 'fluid.la'
http.is_version_visible(server)
http.is_version_visible(server, ssl=True, port=443)
ssl.is_cert_cn_not_equal_to_site(server)
ssl.is_cert_inactive(server)
ssl.is_cert_validity_lifespan_unsafe(server)
ssl.is_pfs_disabled(server)
ssl.is_sslv3_enabled(server)
ssl.is_tlsv1_enabled(server)

# dns.has_cache_poison(server, 'ns-79.awsdns-09.com.')
# dns.has_recursion('ns-79.awsdns-09.com.')
#
# server = 'smtp.gmail.com'
# ssl.is_cert_cn_not_equal_to_site(server, port=993)
# ssl.is_cert_inactive(server, port=993)
# ssl.is_cert_validity_lifespan_unsafe(server, port=993)
# ssl.is_pfs_disabled(server, port=993)
# ssl.is_sslv3_enabled(server, port=993)
# ssl.is_tlsv1_enabled(server, port=993)
