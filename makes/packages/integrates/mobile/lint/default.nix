{ integratesPkgs
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  arguments = {
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
    envSrcIntegratesMobile = path "/integrates/mobile";
  };
  builder = path "/makes/packages/integrates/mobile/lint/builder.sh";
  name = "integrates-mobile-lint";
  searchPaths = {
    envPaths = [
      integratesPkgs.bash
      integratesPkgs.nodejs-12_x
    ];
  };
}
