let
  pkgs = import ../build/pkgs/sorts.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;

  sortsDependencies = import ../build/src/sorts-dependencies.nix pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "sorts";

    buildInputs = sortsDependencies.runtime;

    pyPkgSorts = builders.pythonPackageLocal {
      path = ../sorts;
      python = pkgs.python38;
    };
  }
