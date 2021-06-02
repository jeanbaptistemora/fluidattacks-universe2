{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "skims-test-cli";
  searchPaths = {
    envPaths = [
      nixpkgs.gnugrep
      packages.skims
    ];
  };
  template = path "/makes/applications/skims/test/cli/entrypoint.sh";
}
