pkgs:

let
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;

  customPkgs.python = import ../pkgs/python pkgs;
in
  (import ./deploy-container.nix pkgs)
  ++ [
    customPkgs.python
    pkgs.cacert
    pkgs.curl
    pkgs.docker
    pkgs.firefox
    pkgs.geckodriver
    pkgs.hostname
    pkgs.jq
    pkgs.kubectl
    pkgs.nix-linter
    pkgs.nodejs
    pkgs.openjdk
    pkgs.redis
    pkgs.rpl
    pkgs.shellcheck
    pkgs.terraform
    pkgs.tflint
    pkgs.unzip
    pkgs.wget
    pkgs.zip
  ]
