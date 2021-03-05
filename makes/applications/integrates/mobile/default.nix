{ nixpkgs2
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
      nixpkgs2.findutils
      nixpkgs2.iproute
      nixpkgs2.nodejs-12_x
      nixpkgs2.xdg_utils
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/entrypoint.sh";
}
