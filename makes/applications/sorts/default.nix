{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "sorts";
  searchPaths = {
    envSources = [ packages.sorts.config-runtime ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/sorts/entrypoint.sh";
}
