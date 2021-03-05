{ nixpkgs
, path
, makeEntrypoint
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [ nixpkgs.docker ];
  };
  name = "forces-test-container";
  template = path "/makes/applications/forces/test-container/entrypoint.sh";
}
