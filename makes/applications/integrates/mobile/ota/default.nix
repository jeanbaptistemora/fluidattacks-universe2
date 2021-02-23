{ integratesMobilePkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint integratesMobilePkgs {
  arguments = {
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile-ota";
  searchPaths = {
    envPaths = [
      integratesMobilePkgs.findutils
      integratesMobilePkgs.gnused
      integratesMobilePkgs.nodejs-12_x
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/ota/entrypoint.sh";
}
