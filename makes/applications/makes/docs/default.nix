{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
} @ _:
makeEntrypoint makesPkgs {
  name = "makes-docs";
  arguments = {
    envRuntime = packages.makes.docs.runtime;
  };
  searchPaths = {
    envPaths = [
      makesPkgs.nodejs
    ];
  };
  template = path "/makes/applications/makes/docs/entrypoint.sh";
}
