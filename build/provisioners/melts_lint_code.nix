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
        pkgs.python37
      ];

      pyPkgProspector = builders.pythonPackage {
        requirement = "prospector[with_everything]==1.3.0";
      };
      pyPkgMypy = builders.pythonPackage {
        requirement = "mypy==0.782";
      };
      pyPkgMelts = import ../../melts pkgs;
    })
  )
