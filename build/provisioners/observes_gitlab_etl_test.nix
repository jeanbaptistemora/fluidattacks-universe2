let
  pkgs = import ../pkgs/observes.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;

in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "gitlab_etl";

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

          EtlGitlab = pkgs.poetry2nix.mkPoetryEnv {
            projectDir = ../../observes/etl/dif_gitlab_etl;
            python = pkgs.python38;
          };

        })
  )
