{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-kill";
  searchPaths = {
    envPaths = [
      packages.makes.kill-port
    ];
  };
  template = path "/makes/applications/integrates/kill/entrypoint.sh";
}
