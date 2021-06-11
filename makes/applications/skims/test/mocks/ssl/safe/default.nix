{ nixpkgs
, makeEntrypoint
, makeTemplate
, path
, sslCerts
, ...
}:
makeEntrypoint {
  arguments = {
    envConfig = makeTemplate {
      arguments = {
        envHttpServerSslCert = sslCerts {
          name = "skims-test-mocks-ssl-safe";
          options = [ "-subj" "/CN=localhost" ];
        };
        envHttpServerRoot = path "/makes/applications/skims/test/mocks/ssl/http/server/root";
      };
      name = "nginx-conf";
      template = ''
        events {}
        daemon off;
        http {
          server {
            index index.html;
            listen localhost:4445 ssl;
            location / {
              root __envHttpServerRoot__;
            }
            server_name localhost;
            ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
            ssl_certificate __envHttpServerSslCert__/cert.crt;
            ssl_certificate_key __envHttpServerSslCert__/cert.key;
            ssl_ecdh_curve secp384r1;
            ssl_prefer_server_ciphers on;
            ssl_protocols TLSv1.3;
          }
        }
        pid /dev/null;
      '';
    };
  };
  name = "skims-test-mocks-ssl-safe";
  searchPaths = {
    envLibraries = [
      nixpkgs.openssl.out
    ];
    envPaths = [
      nixpkgs.nginxLocal
    ];
  };
  template = "nginx -c __envConfig__";
}
