{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "docs-deploy";
  arguments = {
    envRuntime = packages.docs.runtime;
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
  template = path "/makes/applications/docs/deploy/entrypoint.sh";
}
