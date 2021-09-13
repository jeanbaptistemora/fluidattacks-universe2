{ nixpkgs
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
      nixpkgs.bash
      nixpkgs.nodejs-12_x
    ];
    envSources = [ packages.integrates.mobile.config.dev-runtime-env ];
  };
}
