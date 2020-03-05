let
  pkgs = import ./pkgs/stable.nix;
  builders.nodejsModule = import ./builders/nodejs-module pkgs;
  builders.pythonPackage = import ./builders/python-package pkgs;
  builders.pythonPackageLocal = import ./builders/python-package-local pkgs;
  builders.pythonRequirements = import ./builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation ({}
    // (import ./src/basic.nix pkgs)
    // (import ./src/dynamodb-local.nix pkgs)
    // (import ./src/external.nix pkgs)
    // rec {
      name = "builder";

      buildInputs = import ./dependencies/full.nix pkgs;

      pkgGeckoDriver = pkgs.geckodriver;
      pkgFirefox = pkgs.firefox;

      nodejsModuleGraphqlSchemaLinter =
        builders.nodejsModule "graphql-schema-linter@0.2.4";
      pyPkgIntegratesBack =
        builders.pythonPackageLocal ../django-apps/integrates-back;
      pyPkgReqs =
        builders.pythonRequirements ./dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../deploy/containers/deps-app/requirements.txt;

      pyAsyncPkgReqs =
        builders.pythonRequirements ./dependencies/requirements-async.txt;
      pyAsyncPkgReqsApp =
        builders.pythonRequirements ../deploy/containers/deps-app/requirements.txt;
      pyAsyncPkgIntegratesBack =
        builders.pythonPackageLocal ../django-apps/integrates-back-async;

      srcDerivationsCerts = import ./derivations/certs pkgs;
    }
  )
