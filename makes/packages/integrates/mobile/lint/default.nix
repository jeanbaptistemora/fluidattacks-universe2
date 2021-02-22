{ integratesMobilePkgs
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesMobilePkgs {
  arguments = {
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
    envSrcIntegratesMobile = path "/integrates/mobile";
  };
  builder = path "/makes/packages/integrates/mobile/lint/builder.sh";
  name = "integrates-mobile-lint";
  searchPaths = {
    envPaths = [
      integratesMobilePkgs.bash
      integratesMobilePkgs.nodejs-12_x
    ];
  };
}
