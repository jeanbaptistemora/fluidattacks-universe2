{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
}:
makeEntrypoint makesPkgs {
  name = "makes-done";
  searchPaths = {
    envPaths = [
      makesPkgs.netcat
      packages.makes.kill-port
    ];
  };
  template = path "/makes/applications/makes/done/entrypoint.sh";
}
