{ nixpkgs
, makeEntrypoint
, makeTemplate
, path
, sslCerts
, packages
, ...
}:
makeEntrypoint {
  arguments = {
    envConfig = makeTemplate {
      arguments = {
        envHttpServerSslCert = sslCerts {
          name = "skims-test-mocks-ssl-unsafe";
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
            listen localhost:4446 ssl;
            location / {
              root __envHttpServerRoot__;
            }
            server_name localhost;
            ssl_prefer_server_ciphers off;
            ssl_ciphers "ADH-AES128-SHA:ADH-AES256-SHA:ADH-CAMELLIA128-SHA:ADH-CAMELLIA256-SHA:ADH-DES-CBC3-SHA:ADH-RC4-MD5:ADH-SEED-SHA:AES128-SHA:AES256-SHA:CAMELLIA128-SHA:ADH-SEED-SHA:AES128-SHA:AES256-SHA:CAMELLIA128-SHA:DH-DSS-AES256-SHA:DH-DSS-CAMELLIA128-SHA:DH-DSS-CAMELLIA256-SHA:DH-DSS-DES-CBC3-SHA:DH-DSS-SEED-SHA:DES-CBC3-SHA:aNULL:eNULL:EXPORT:DES:MD5:PSK:RC4";
            ssl_certificate __envHttpServerSslCert__/cert.crt;
            ssl_certificate_key __envHttpServerSslCert__/cert.key;
            ssl_protocols SSLv3 TLSv1 TLSv1.1;
          }
        }
        pid /dev/null;
      '';
    };
  };
  name = "skims-test-mocks-ssl-unsafe";
  searchPaths = {
    envPaths = [
      packages.makes.kill-port
      nixpkgs.nginxLocal
    ];
  };
  template = path "/makes/applications/skims/test/mocks/ssl/unsafe/entrypoint.sh";
}
