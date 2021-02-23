{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
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
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/analytics/documents/entrypoint.sh";
}
