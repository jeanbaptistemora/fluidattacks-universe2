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
  name = "integrates-subscriptions-user-to-entity";
  searchPaths = {
    envPaths = [
      nixpkgs2.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
    ];
  };
  template = path "/makes/applications/integrates/subscriptions/user-to-entity/entrypoint.sh";
}
