{
  inputs,
  makeScript,
  makeSslCertificate,
  makeTemplate,
  managePorts,
  ...
}:
makeScript {
  replace = {
    __argConfig__ = makeTemplate {
      replace = {
        __argHttpServerSslCert__ = makeSslCertificate {
          days = 365;
          name = "skims-test-mocks-ssl-proxy";
          options = [["-subj" "/CN=localhost"]];
        };
        __argHttpServerRoot__ = ../http/server/root;
      };
      name = "nginx-conf";
      template = ''
        events {}
        daemon off;
        http {
          server {
            listen localhost:4447 ssl;
            location / {
              root __argHttpServerRoot__;
              proxy_pass https://localhost:4446;
            }
            server_name localhostproxy;
            ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
            ssl_certificate __argHttpServerSslCert__/cert.crt;
            ssl_certificate_key __argHttpServerSslCert__/cert.key;
            ssl_ecdh_curve secp384r1;
            ssl_prefer_server_ciphers on;
            ssl_protocols TLSv1.3;
          }
        }
        pid /dev/null;
      '';
    };
  };
  name = "skims-test-mocks-ssl-proxy";
  searchPaths = {
    bin = [
      inputs.nixpkgs.nginxLocal
    ];
    source = [
      managePorts
    ];
    rpath = [inputs.nixpkgs.openssl.out];
  };
  entrypoint = ./entrypoint.sh;
}
