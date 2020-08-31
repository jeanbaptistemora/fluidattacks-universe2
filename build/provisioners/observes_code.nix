let
  pkgs = import ../pkgs/stable.nix;
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
            pkgs.awscli
            pkgs.sops
            pkgs.jq
            pkgs.python37
            pkgs.python37Packages.GitPython
            pkgs.python37Packages.psycopg2
          ];

          pyPkgAioextensions = builders.pythonPackage {
            requirement = "aioextensions==20.8.2087641";
          };
          pyPkgFluidCLI = builders.pythonPackage {
            requirement = "fluidattacks";
          };

          # Constants for dynamic linked binaries
          LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib64:$LD_LIBRARY_PATH";
        })
  )
