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
            pkgs.python38Packages.poetry
          ];

          pyPkgMypy = builders.pythonPackage {
            requirement = "mypy==0.782";
          };

          pyPkgProspector = builders.pythonPackage {
            requirement = "prospector==1.3.0";
          };

          pyPkgPytest = builders.pythonPackage {
            requirement = "pytest==6.1.0";
          };

          pyPkgEtlGitlab = builders.pythonPackageLocal {
            path = ../../observes/etl/dif_gitlab_etl;
          };

          pyPkgStreamerGitlab = builders.pythonPackageLocal {
            path = ../../observes/singer/streamer_gitlab;
          };

          pyPkgTapJson = builders.pythonPackageLocal {
            path = ../../observes/singer/tap_json;
          };

          pyPkgTargetRedshift = builders.pythonPackageLocal {
            path = ../../observes/singer/target_redshift;
          };

        })
  )
