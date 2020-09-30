let
  pkgs = import ../build/pkgs/observes.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "observers";

    buildInputs = [
      pkgs.git
      pkgs.awscli
      pkgs.sops
      pkgs.jq
      pkgs.python38Packages.psycopg2
    ];

    pyPkgTapJson = builders.pythonPackageLocal {
      path = ../observes/singer/tap_json;
      python = pkgs.python38;
    };

    pyPkgTargetRedshift = builders.pythonPackageLocal {
      path = ../observes/singer/target_redshift;
      python = pkgs.python38;
    };

    # Constants for dynamic linked binaries
    LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
  }
