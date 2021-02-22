{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-back-test-unit";
  searchPaths = {
    envPaths = [
      packages.integrates.cache
      packages.integrates.db
      packages.integrates.storage
    ];
    envSources = [
      packages.integrates.back.pypi.development
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/back/test/unit/entrypoint.sh";
}
