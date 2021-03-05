{ nixpkgs2
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-cache";
  searchPaths = {
    envPaths = [
      nixpkgs2.redis
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/cache/entrypoint.sh";
}
