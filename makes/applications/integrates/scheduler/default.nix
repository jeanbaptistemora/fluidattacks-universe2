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
  name = "integrates-scheduler";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
    ];
  };
  template = path "/makes/applications/integrates/scheduler/entrypoint.sh";
}
