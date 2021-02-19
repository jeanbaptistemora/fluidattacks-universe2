{ integratesPkgs
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  builder = path "/makes/packages/integrates/front/test/builder.sh";
  envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
  envSrcIntegratesFront = path "/integrates/front";
  name = "integrates-front-test";
  searchPaths = {
    envPaths = [
      integratesPkgs.nodejs
    ];
  };
}
