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
    envSources = [ packages.sorts.config-development ];
  };
  template = path "/makes/applications/sorts/train/entrypoint.sh";
}
