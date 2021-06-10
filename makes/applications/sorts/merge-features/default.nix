{ makeEntrypoint
, packages
, path
, nixpkgs
, ...
}:
makeEntrypoint {
  name = "sorts-merge-features";
  searchPaths = {
    envPaths = [ nixpkgs.python38 ];
    envSources = [
      packages.sorts.config-development
      packages.sorts.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/sorts/merge-features/entrypoint.sh";
}
