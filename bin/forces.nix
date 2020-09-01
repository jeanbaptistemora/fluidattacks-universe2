let
  pkgs = import ../build/pkgs/forces.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "forces";

    buildInputs = [
    ];

    pyPkgForces = builders.pythonPackageLocal {
      path = ../forces;
      python = pkgs.python38;
    };
  }
