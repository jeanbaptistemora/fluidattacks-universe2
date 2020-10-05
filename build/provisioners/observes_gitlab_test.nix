let
  pkgs = import ../pkgs/observes.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;

in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.python38
          ];

          pyPkgMypy = builders.pythonPackage {
            requirement = "mypy==0.782";
            python = pkgs.python38;
          };

          pyPkgProspector = builders.pythonPackage {
            requirement = "prospector==1.3.0";
            python = pkgs.python38;
          };

          pyPkgPytest = builders.pythonPackage {
            requirement = "pytest==6.1.0";
            python = pkgs.python38;
          };

          pyPkgTapGitlab = builders.pythonPackageLocal {
            path = ../../observes/singer/streamer_gitlab;
            python = pkgs.python38;
          };
        })
  )
