{ makeEntrypoint
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envRoot = path "/";
  };
  name = "makes-attrs";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
    ];
  };
  template = path "/makes/applications/makes/attrs/template.sh";
}
