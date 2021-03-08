{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "sorts";
  searchPaths = {
    envSources = [ packages.sorts.config-runtime ];
  };
  template = path "/makes/applications/sorts/entrypoint.sh";
}
