pkgs:

let
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;

  customPkgs.python = import ../pkgs/python pkgs;
in
  [
    customPkgs.python
    pkgs.awscli
    pkgs.cacert
    pkgs.curl
    pkgs.docker
    pkgs.git
    pkgs.hostname
    pkgs.jq
    pkgs.nodejs
    pkgs.openjdk
    pkgs.redis
    pkgs.sops
    pkgs.unzip
  ]
