{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "melts";
  searchPaths = {
    envSources = [ packages.melts.config-runtime ];
  };
  template = path "/makes/applications/melts/entrypoint.sh";
}
