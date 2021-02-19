{ integratesPkgs
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  builder = path "/makes/packages/integrates/front/lint/stylelint/builder.sh";
  envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
  envSrcIntegratesFront = path "/integrates/front";
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    envPaths = [
      integratesPkgs.nodejs
    ];
  };
}
