from fluidasserts.service import http
from fluidasserts.service import http_ssl
from fluidasserts.service import moddns

#server = '127.0.0.1'
server = 'fluid.la'
http.is_version_visible(server)
http_ssl.is_cert_inactive(server)
http_ssl.is_cert_validity_lifespan_unsafe(server)
http_ssl.is_pfs_disabled(server)
http_ssl.is_sslv3_enabled(server)
http_ssl.is_tlsv1_enabled(server)
