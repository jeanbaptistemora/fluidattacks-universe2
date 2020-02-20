pkgs:

let
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;

  customPkgs.python = import ../pkgs/python pkgs;
in
  [
    customPkgs.python
    pkgs.awscli
    pkgs.git
    pkgs.openjdk
    pkgs.unzip
  ]
