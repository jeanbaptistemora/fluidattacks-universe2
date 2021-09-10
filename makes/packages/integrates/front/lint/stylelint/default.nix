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
  builder = path "/makes/packages/integrates/front/lint/stylelint/builder.sh";
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    envPaths = [ nixpkgs.nodejs ];
    envSources = [ packages.integrates.front.config.dev-runtime-env ];
  };
}
