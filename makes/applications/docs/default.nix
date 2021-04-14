{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "docs";
  arguments = {
    envRuntime = packages.docs.runtime;
  };
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
      nixpkgs.xdg_utils
    ];
  };
  template = path "/makes/applications/docs/entrypoint.sh";
}
