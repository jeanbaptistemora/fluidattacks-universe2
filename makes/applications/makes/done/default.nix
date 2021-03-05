{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "makes-done";
  searchPaths = {
    envPaths = [
      nixpkgs.netcat
      packages.makes.kill-port
    ];
  };
  template = path "/makes/applications/makes/done/entrypoint.sh";
}
