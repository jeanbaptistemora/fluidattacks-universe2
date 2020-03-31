let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.glibcLocales
        pkgs.awscli
      ];
    })
  )
