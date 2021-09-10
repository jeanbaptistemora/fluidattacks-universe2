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
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/sorts/execute/entrypoint.sh";
}
