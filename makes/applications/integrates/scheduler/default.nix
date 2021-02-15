{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envIntegratesEnv = packages."integrates/back/env";
  };
  name = "integrates-scheduler";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/scheduler/entrypoint.sh";
}
