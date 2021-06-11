{ nixpkgs
, makeEntrypoint
, path
, ...
}:
let
  httpServerListen = "localhost:4445";
  httpServerRoot = path "/makes/applications/skims/test/mocks/ssl/http/server/root";
in
makeEntrypoint {
  arguments = {
    envConfig = builtins.toFile "nginx.conf" ''
      events {}
      daemon off;
      http {
        server {
          index index.html;
          listen ${httpServerListen};
          location / {
            root ${httpServerRoot};
          }
          server_name localhost;
        }
      }
      pid /dev/null;
    '';
  };
  name = "skims-test-mocks-ssl-safe";
  searchPaths = {
    envPaths = [
      nixpkgs.nginxLocal
    ];
  };
  template = "echo http://${httpServerListen} && nginx -c __envConfig__";
}
