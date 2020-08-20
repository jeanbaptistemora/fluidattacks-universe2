let
  pkgs = import ../pkgs/stable.nix;
  old-pkgs = import ../pkgs/old.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.shellcheck
            old-pkgs.nix-linter
          ];

          pyPkgMypy = builders.pythonPackage "mypy==0.782";
          pyPkgProspector = builders.pythonPackage "prospector[with_everything]==1.2.0";
        })
  )


