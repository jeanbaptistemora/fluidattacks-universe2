{ makeEntrypoint
, packages
, path
, nixpkgs
, ...
}:
makeEntrypoint {
  name = "sorts-train";
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
  template = path "/makes/applications/sorts/train/entrypoint.sh";
}
