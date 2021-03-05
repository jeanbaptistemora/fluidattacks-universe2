{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
  };
  name = "integrates-subscriptions-user-to-entity";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
    ];
  };
  template = path "/makes/applications/integrates/subscriptions/user-to-entity/entrypoint.sh";
}
