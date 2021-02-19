{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile-ota";
  searchPaths = {
    envPaths = [
      integratesPkgs.findutils
      integratesPkgs.gnused
      integratesPkgs.nodejs-12_x
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/ota/entrypoint.sh";
}
