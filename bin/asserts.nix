let
  pkgs = import ../build/pkgs/asserts.nix;

  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "asserts";

    buildInputs = [
      pkgs.git
      pkgs.awscli
      pkgs.sops
      pkgs.jq
      pkgs.postgresql
      pkgs.python37
    ];

    pyPkgAsserts = builders.pythonPackageLocal {
      path = ../asserts;
      python = pkgs.python38;
      requirements = [
        pkgs.unixODBC
      ];
    };
  }
