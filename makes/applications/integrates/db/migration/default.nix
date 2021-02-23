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
  name = "integrates-db-migration";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
    ];
  };
  template = path "/makes/applications/integrates/db/migration/entrypoint.sh";
}
