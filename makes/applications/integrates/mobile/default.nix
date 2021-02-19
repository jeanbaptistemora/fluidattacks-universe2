{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSetupIntegratesMobileDevRuntime = packages.integrates.mobile.config.dev-runtime;
  };
  name = "integrates-mobile";
  searchPaths = {
    envPaths = [
      integratesPkgs.findutils
      integratesPkgs.iproute
      integratesPkgs.nodejs-12_x
      integratesPkgs.xdg_utils
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/mobile/entrypoint.sh";
}
