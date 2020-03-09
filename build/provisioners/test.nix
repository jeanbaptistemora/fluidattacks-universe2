let
  pkgs = import ../pkgs/stable.nix;

  builders.nodejsModule = import ../builders/nodejs-module pkgs;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../dependencies/requirements.nix pkgs)
    // (import ../dependencies/requirements-async.nix pkgs)
    // (import ../src/basic.nix)
    // (import ../src/dynamodb-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/nodejs.nix pkgs)
        ++ (import ../dependencies/python-with-tools.nix pkgs)
        ++ (import ../dependencies/secret-management.nix pkgs)
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.cacert
          pkgs.openjdk
          pkgs.redis
          pkgs.unzip
        ];
    })
  )
