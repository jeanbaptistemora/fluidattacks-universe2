{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "makes-doc";
  arguments = {
    envRuntime = packages.makes.doc.runtime;
  };
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
      nixpkgs.xdg_utils
    ];
  };
  template = path "/makes/applications/makes/doc/entrypoint.sh";
}
