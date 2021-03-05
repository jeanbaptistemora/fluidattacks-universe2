{ nixpkgs2
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-analytics-documents";
  searchPaths = {
    envPaths = [
      nixpkgs2.findutils
      nixpkgs2.python37
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
