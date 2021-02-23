{ makeEntrypoint
, makesPkgs
, packages
, path
, ...
} @ _:
makeEntrypoint makesPkgs {
  name = "makes-docs-deploy";
  arguments = {
    envRuntime = packages.makes.docs.runtime;
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
  template = path "/makes/applications/makes/docs/deploy/entrypoint.sh";
}
