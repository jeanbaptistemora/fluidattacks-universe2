{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "integrates-cache";
  searchPaths = {
    envPaths = [
      nixpkgs.redis
      packages.makes.done
      packages.makes.kill-port
      packages.makes.wait
    ];
  };
  template = path "/makes/applications/integrates/cache/entrypoint.sh";
}
