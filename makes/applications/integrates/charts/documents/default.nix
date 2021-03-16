{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-charts-documents";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/charts/documents/entrypoint.sh";
}
