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
            pkgs.awscli
            pkgs.cacert
            pkgs.sops
            pkgs.jq
            pkgs.nix
            pkgs.openssh
            pkgs.python37
            pkgs.python37Packages.GitPython
            pkgs.python37Packages.psycopg2
            melts
          ];

          pyPkgAioextensions = builders.pythonPackage {
            requirement = "aioextensions==20.8.2087641";
          };
          pyPkgRequests= builders.pythonPackage {
            requirement = "requests==2.25.1";
          };
          melts = (import ../..).melts;
          srcProduct = (import ../..).product;
        })
  )
