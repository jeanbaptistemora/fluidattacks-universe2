{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint {
  arguments = {
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile-build-ios";
  searchPaths = {
    envPaths = [
      nixpkgs.curl
      nixpkgs.nodejs-12_x
    ];
    envSources = [ packages.integrates.mobile.config.dev-runtime-env ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/build/ios/entrypoint.sh";
}
