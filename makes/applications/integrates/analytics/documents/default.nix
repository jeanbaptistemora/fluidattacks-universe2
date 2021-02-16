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
  name = "integrates-analytics-documents";
  searchPaths = {
    envPaths = [
      integratesPkgs.findutils
      integratesPkgs.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
      packages.makes.kill-port
      packages.makes.wait
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/analytics/documents/entrypoint.sh";
}
