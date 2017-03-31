from fluidasserts.service import http
from fluidasserts.service import http_ssl
from fluidasserts.service import moddns

#server = '127.0.0.1'
url = 'https://fluid.la'
#server = 'fluid.la'
#http.is_version_visible(server)
#http_ssl.is_cert_inactive(server)
#http_ssl.is_cert_validity_lifespan_unsafe(server)
#http_ssl.is_pfs_disabled(server)
#http_ssl.is_sslv3_enabled(server)
#http_ssl.is_tlsv1_enabled(server)
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
http.is_header_x_permitted_cross_domain_policies_missing(url)
http.is_header_x_xxs_protection_missing(url)
http.is_header_hsts_missing(url)
http.is_basic_auth_enabled(url)
http.has_trace_method(url)
http.has_delete_method(url)
http.has_put_method(url)
http.is_sessionid_exposed(url)
