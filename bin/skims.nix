let
  pkgs = import ../build/pkgs/skims.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "skims";

    buildInputs = [
    ];

    pyPkgSkims = builders.pythonPackageLocal {
      path = ../skims;
      python = pkgs.python38;
    };
  }
