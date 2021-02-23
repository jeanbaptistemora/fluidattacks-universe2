{ assertsPkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint assertsPkgs {
  name = "asserts";
  searchPaths = {
    envSources = [ packages.asserts.env ];
  };
  template = path "/makes/applications/asserts/entrypoint.sh";
}
