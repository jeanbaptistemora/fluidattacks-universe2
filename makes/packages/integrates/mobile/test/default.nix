{ integratesMobilePkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation integratesMobilePkgs {
  arguments = {
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
    envSrcIntegratesMobile = path "/integrates/mobile";
  };
  builder = path "/makes/packages/integrates/mobile/test/builder.sh";
  name = "integrates-mobile-test";
  searchPaths = {
    envPaths = [
      integratesMobilePkgs.bash
      integratesMobilePkgs.nodejs-12_x
    ];
  };
}
