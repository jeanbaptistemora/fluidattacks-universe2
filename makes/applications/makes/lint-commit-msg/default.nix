{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      nixpkgs.git
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
