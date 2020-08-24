let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.python38
            pkgs.shellcheck
          ];

          pyPkgMypy = builders.pythonPackage {
            requirement = "mypy==0.782";
          };
          pyPkgProspector = builders.pythonPackage {
            requirement = "prospector[with_everything]==1.2.0";
          };
        })
  )


