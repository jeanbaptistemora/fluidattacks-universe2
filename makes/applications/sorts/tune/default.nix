{ makeEntrypoint
, packages
, path
, nixpkgs
, ...
}:
makeEntrypoint {
  name = "sorts-tune";
  searchPaths = {
    envPaths = [ nixpkgs.python38 ];
    envSources = [
      packages.sorts.config-development
      packages.sorts.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/sorts/tune/entrypoint.sh";
}
