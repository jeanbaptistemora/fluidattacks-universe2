{ forcesPkgs
, path
, makeEntrypoint
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [ forcesPkgs.docker ];
  };
  name = "forces-test-container";
  template = path "/makes/applications/forces/test-container/entrypoint.sh";
}
