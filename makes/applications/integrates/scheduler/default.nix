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
  name = "integrates-scheduler";
  searchPaths = {
    envPaths = [
      nixpkgs.python37
    ];
  };
  template = path "/makes/applications/integrates/scheduler/entrypoint.sh";
}
