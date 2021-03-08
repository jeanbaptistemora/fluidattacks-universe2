{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSrcSortsSorts = path "/sorts/sorts";
  };
  name = "sorts-test";
  searchPaths = {
    envSources = [
      packages.sorts.config-development
      packages.sorts.config-runtime
    ];
  };
  template = path "/makes/applications/sorts/test/entrypoint.sh";
}
