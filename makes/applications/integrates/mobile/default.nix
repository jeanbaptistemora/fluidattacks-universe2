{ integratesMobilePkgs
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
      integratesMobilePkgs.findutils
      integratesMobilePkgs.iproute
      integratesMobilePkgs.nodejs-12_x
      integratesMobilePkgs.xdg_utils
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/entrypoint.sh";
}
