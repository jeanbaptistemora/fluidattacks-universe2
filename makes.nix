# For more information visit:
# https://github.com/fluidattacks/makes
{
  fetchNixpkgs,
  projectPath,
  ...
}: {
  cache = {
    readAndWrite = {
      enable = true;
      name = "fluidattacks";
      pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
    };
  };
  extendingMakesDir = "/makes/foss/units";
  imports = [
    ./airs/makes.nix
    ./common/makes.nix
    ./docs/makes.nix
    ./forces/makes.nix
    ./makes/foss/modules/makes.nix
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
            configureFlags =
              attrs.configureFlags
              ++ [
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
    flakeAdapter = import (builtins.fetchTarball {
      url = "https://github.com/edolstra/flake-compat/archive/12c64ca55c1014cdc1b16ed5a804aa8576601ff2.tar.gz";
      sha256 = "0jm6nzb83wa6ai17ly9fzpqc40wg1viib8klq8lby54agpl213w5";
    });
    product = import (projectPath "/");
  };
}
