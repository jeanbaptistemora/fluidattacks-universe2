let
  pkgs = import ../pkgs/melts.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.python37
      ];
      pyPkgTwine = builders.pythonPackage {
          requirement = "twine==3.2.0";
      };
    })
  )