let
  pkgs = import ../pkgs/stable.nix;

  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../dependencies/requirements.nix pkgs)
    // (import ../src/basic.nix)
    // (import ../src/dynamodb-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/python-with-tools.nix pkgs)
        ++ (import ../dependencies/secret-management.nix pkgs)
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.openjdk
          pkgs.redis
          pkgs.unzip
          pkgs.nodejs
        ];
    })
  )
