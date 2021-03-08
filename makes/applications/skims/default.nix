{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "skims";
  searchPaths = {
    envSources = [ packages.skims.config-runtime ];
  };
  template = path "/makes/applications/skims/entrypoint.sh";
}
