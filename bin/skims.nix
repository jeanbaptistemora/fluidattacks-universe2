let
  pkgs = import ../build/pkgs/stable.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "bin";

    buildInputs = [
    ];

    pyPkgSkims = builders.pythonPackageLocal ../skims;
  }
