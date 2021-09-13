{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.iproute
      nixpkgs.nodejs-12_x
      nixpkgs.xdg_utils
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
    envSources = [ packages.integrates.mobile.config.dev-runtime-env ];
  };
  template = path "/makes/applications/integrates/mobile/entrypoint.sh";
}
