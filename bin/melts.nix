let
  pkgs = import ../build/pkgs/melts.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "melts";

    buildInputs = [
    ];

    pyPkgMelts = builders.pythonPackageLocal {
      path = ../melts;
      python = pkgs.python38;
    };

    # Constants for dynamic linked binaries
    LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
  }
