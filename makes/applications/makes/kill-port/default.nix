{ makeEntrypoint
, makesPkgs
, path
, ...
}:
makeEntrypoint {
  name = "makes-kill-port";
  searchPaths = {
    envPaths = [
      makesPkgs.lsof
    ];
  };
  template = path "/makes/applications/makes/kill-port/entrypoint.sh";
}
