{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = { };
  name = "integrates-scheduler";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
    ];
    envSources = [
      packages."integrates/secrets/list"
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/scheduler/entrypoint.sh";
}
