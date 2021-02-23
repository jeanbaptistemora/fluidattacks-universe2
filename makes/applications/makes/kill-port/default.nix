{ makeEntrypoint
, makesPkgs
, path
, ...
}:
makeEntrypoint makesPkgs {
  name = "makes-kill-port";
  searchPaths = {
    envPaths = [
      makesPkgs.lsof
    ];
  };
  template = path "/makes/applications/makes/kill-port/entrypoint.sh";
}
