{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-db-migration";
  template = path "/makes/applications/integrates/db/migration/entrypoint.sh";
}
