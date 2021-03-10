{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "melts-test";
  searchPaths = {
    envSources = [
      packages.melts.config-development
      packages.melts.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
    ];
    envPaths = [
      nixpkgs.gnugrep
    ];
  };
  template = path "/makes/applications/melts/test/entrypoint.sh";
}
