{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "asserts";
  searchPaths = {
    envSources = [ packages.asserts.env ];
  };
  template = path "/makes/applications/asserts/entrypoint.sh";
}
