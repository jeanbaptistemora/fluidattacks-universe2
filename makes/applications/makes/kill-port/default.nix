{ makeEntrypoint
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  name = "makes-kill-port";
  searchPaths = {
    envPaths = [
      nixpkgs.lsof
    ];
  };
  template = path "/makes/applications/makes/kill-port/entrypoint.sh";
}
