{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
} @ _:
makeEntrypoint makesPkgs {
  name = "makes-doc-deploy";
  arguments = {
    envRuntime = packages.makes.doc.runtime;
  };
  searchPaths = {
    envPaths = [
      makesPkgs.awscli
      makesPkgs.nodejs
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/makes/doc/deploy/entrypoint.sh";
}
