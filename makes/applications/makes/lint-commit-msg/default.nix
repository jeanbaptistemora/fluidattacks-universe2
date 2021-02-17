{ makesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint makesPkgs {
  searchPaths = {
    envPaths = [
      makesPkgs.git
      makesPkgs.nodejs
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
