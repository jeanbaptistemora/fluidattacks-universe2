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
            ssl_ciphers "HIGH:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK:!RC4";
            ssl_certificate __envHttpServerSslCert__/cert.crt;
            ssl_certificate_key __envHttpServerSslCert__/cert.key;
            ssl_protocols TLSv1.2 TLSv1.3;
          }
        }
        pid /dev/null;
      '';
    };
  };
  name = "skims-test-mocks-ssl-safe";
  searchPaths = {
    envPaths = [
      nixpkgs.nginxLocal
    ];
  };
  template = "nginx -c __envConfig__";
}
