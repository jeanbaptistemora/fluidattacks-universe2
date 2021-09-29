# For more information visit:
# https://github.com/fluidattacks/makes
{ fetchNixpkgs
, projectPath
, ...
}:
{
  cache = {
    readAndWrite = {
      enable = true;
      name = "fluidattacks";
      pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
    };
  };
  extendingMakesDir = "/makes/foss/units";
  imports = [
    ./makes/foss/modules/makes.nix

    ./makes/foss/extra-modules/legacy.nix
  ];
  inputs = {
    nixpkgs = fetchNixpkgs {
      rev = "f88fc7a04249cf230377dd11e04bf125d45e9abe";
      sha256 = "1dkwcsgwyi76s1dqbrxll83a232h9ljwn4cps88w9fam68rf8qv3";
      overlays = [
        (_: supper: {
          # Nginx by default tries to use directories owned by root
          # We have to recompile it pointing to the user-space
          nginxLocal = supper.nginx.overrideAttrs (attrs: {
            configureFlags = attrs.configureFlags ++ [
              "--error-log-path=/tmp/error.log"
              "--http-client-body-temp-path=/tmp/nginx_client_body"
              "--http-fastcgi-temp-path=/tmp/nginx_fastcgi"
              "--http-log-path=/tmp/access.log"
              "--http-proxy-temp-path=/tmp/nginx_proxy"
              "--http-scgi-temp-path=/tmp/nginx_scgi"
              "--http-uwsgi-temp-path=/tmp/nginx_uwsgi"
            ];
          });
        })
      ];
    };
    product = import (projectPath "/");
  };
}
