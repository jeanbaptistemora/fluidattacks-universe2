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
  builder = path "/makes/packages/integrates/front/lint/eslint/builder.sh";
  name = "integrates-front-lint-eslint";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
    ];
    envUtils = [ "/makes/utils/lint-typescript" ];
    envSources = [ packages.integrates.front.config.dev-runtime-env ];
  };
}
