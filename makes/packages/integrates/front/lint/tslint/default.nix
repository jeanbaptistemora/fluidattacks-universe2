{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envSrcIntegratesFront = path "/integrates/front";
  };
  builder = path "/makes/packages/integrates/front/lint/tslint/builder.sh";
  name = "integrates-front-lint-tslint";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
  };
}
