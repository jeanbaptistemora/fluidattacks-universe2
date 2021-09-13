{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile-ota";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
      nixpkgs.nodejs-12_x
      nixpkgs.openssl
      packages.makes.announce.bugsnag
    ];
    envSources = [ packages.integrates.mobile.config.dev-runtime-env ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/ota/entrypoint.sh";
}
