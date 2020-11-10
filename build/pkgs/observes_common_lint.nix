let
  pkgs = import ../pkgs/observes.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
          (import ../src/basic.nix)
      //  (rec {
            name = "common_lint";

            buildInputs = [
              pkgs.git
              pkgs.python38
            ];

            pyPkgMypy = builders.pythonPackage {
              requirement = "mypy==0.782";
            };

            pyPkgProspector = builders.pythonPackage {
              requirement = "prospector==1.3.0";
            };

          })
    )
