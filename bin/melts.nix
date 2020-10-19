let
  pkgs = import ../build/pkgs/melts.nix;
  asserts_pkgs = import ./asserts.nix;
  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "melts";

    buildInputs = [
      pkgs.git
      pkgs.awscli
      pkgs.sops
      pkgs.jq
      pkgs.python38Packages.psycopg2
    ];

    pyPkgAsserts = asserts_pkgs.pyPkgAsserts;

    pyPkgMelts = builders.pythonPackageLocal {
      path = ../melts;
      python = pkgs.python38;
    };

    # Constants for dynamic linked binaries
    LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
  }
