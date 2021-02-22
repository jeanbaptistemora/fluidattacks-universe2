{ forcesPkgs
, path
, makeEntrypoint
, ...
} @ _:
makeEntrypoint forcesPkgs {
  searchPaths = {
    envPaths = [ forcesPkgs.docker ];
  };
  name = "forces-test-container";
  template = path "/makes/applications/forces/test-container/entrypoint.sh";
}
