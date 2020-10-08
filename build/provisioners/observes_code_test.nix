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
            pkgs.python38Packages.psycopg2
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

          pyPkgPytestAsync = builders.pythonPackage {
            requirement = "pytest-asyncio==0.14.0";
            python = pkgs.python38;
          };

          pyPkgCode = builders.pythonPackageLocal {
            path = ../../observes/code;
            python = pkgs.python38;
          };
        })
  )
