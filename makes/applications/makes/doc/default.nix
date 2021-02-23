{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
}:
makeEntrypoint makesPkgs {
  name = "makes-doc";
  arguments = {
    envRuntime = packages.makes.doc.runtime;
  };
  searchPaths = {
    envPaths = [
      makesPkgs.nodejs
      makesPkgs.xdg_utils
    ];
  };
  template = path "/makes/applications/makes/doc/entrypoint.sh";
}
