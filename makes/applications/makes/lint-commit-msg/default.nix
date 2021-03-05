{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      makesPkgs.git
    ];
    envNodeBinaries = [
      packages.makes.commitlint
    ];
    envNodeLibraries = [
      packages.makes.commitlint
    ];
  };
  name = "makes-lint-commit-msg";
  template = path "/makes/applications/makes/lint-commit-msg/entrypoint.sh";
}
