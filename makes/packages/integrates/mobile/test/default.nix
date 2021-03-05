{ nixpkgs2
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
    envSrcIntegratesMobile = path "/integrates/mobile";
  };
  builder = path "/makes/packages/integrates/mobile/test/builder.sh";
  name = "integrates-mobile-test";
  searchPaths = {
    envPaths = [
      nixpkgs2.bash
      nixpkgs2.nodejs-12_x
    ];
  };
}
