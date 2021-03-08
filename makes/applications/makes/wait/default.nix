{ makeEntrypoint
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  name = "makes-wait";
  searchPaths = {
    envPaths = [ nixpkgs.netcat ];
  };
  template = path "/makes/applications/makes/wait/entrypoint.sh";
}
