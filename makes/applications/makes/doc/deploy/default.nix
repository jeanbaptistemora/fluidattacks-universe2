{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "makes-doc-deploy";
  arguments = {
    envRuntime = packages.makes.doc.runtime;
  };
  searchPaths = {
    envPaths = [
      nixpkgs.awscli
      nixpkgs.nodejs
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/makes/doc/deploy/entrypoint.sh";
}
