# For more information visit:
# https://github.com/fluidattacks/makes
{fetchNixpkgs, ...}: {
  cache = {
    readAndWrite = {
      enable = true;
      name = "fluidattacks";
      pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
    };
  };
  extendingMakesDirs = ["/"];
  formatBash = {
    enable = true;
    targets = ["/"];
  };
  formatMarkdown = {
    enable = true;
    doctocArgs = ["--title" "# Contents"];
    targets = ["/skims/LICENSE.md"];
  };
  formatNix = {
    enable = true;
    targets = ["/"];
  };
  formatPython = {
    enable = true;
    targets = ["/"];
  };
  formatTerraform = {
    enable = true;
    targets = ["/"];
  };
  formatYaml = {
    enable = true;
    targets = ["/"];
  };
  lintBash = {
    enable = true;
    targets = ["/"];
  };
  lintGitCommitMsg = {
    branch = "trunk";
    enable = true;
    config = "/.lint-git-commit-msg/config.js";
    parser = "/.lint-git-commit-msg/parser.js";
  };
  lintGitMailMap = {
    enable = true;
  };
  lintNix = {
    enable = true;
    targets = ["/"];
  };
  lintTerraform = {
    config = "/.lint-terraform.hcl";
  };
  imports = [
    ./airs/makes.nix
    ./common/makes.nix
    ./docs/makes.nix
    ./forces/makes.nix
    ./integrates/makes.nix
    ./melts/makes.nix
    ./observes/makes.nix
    ./reviews/makes.nix
    ./skims/makes.nix
    ./sorts/makes.nix
  ];
  inputs = {
    nixpkgs = fetchNixpkgs {
      rev = "38130b7dcc46eb6bc4abb161b55e2d29f3a5ef70";
      sha256 = "LaGuYEXI75tKg4tQIv960x5q1AVfFBSfkm48NmIFRHM=";
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
  };
}
