let
  pkgs = import ../build/pkgs/skims.nix;

  builders.pythonPackage = import ../build/builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "skims";

    buildInputs = [
      pkgs.jdk11
    ];

    pyPkgSkims = builders.pythonPackage {
      cacheKey = ../skims;
      python = pkgs.python38;
      requirement = "skims";
    };
  }
