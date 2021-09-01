{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "sorts-extract-features";
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
  template = path "/makes/applications/sorts/extract-features/entrypoint.sh";
}
