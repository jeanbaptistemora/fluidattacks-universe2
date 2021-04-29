{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "sorts-execute";
  searchPaths = {
    envSources = [
      packages.melts.lib
      packages.sorts.config-runtime
    ];
    envUtils = [
      "/makes/utils/git"
    ];
  };
  template = path "/makes/applications/sorts/execute/entrypoint.sh";
}
