let
  pkgs = import ../build/pkgs/sorts.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;

  sortsDependencies = import ../build/src/sorts-dependencies.nix pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "sorts";

    buildInputs = sortsDependencies.runtime;

    pyPkgSorts = builders.pythonPackage {
      cacheKey = ../sorts;
      python = pkgs.python38;
      requirement = "sorts";
    };
  }
