{ makeEntrypoint
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  name = "makes-kill-tree";
  searchPaths = {
    envPaths = [
      nixpkgs.procps
    ];
  };
  template = path "/makes/applications/makes/kill-tree/entrypoint.sh";
}
