{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envSkimsDocsBuild = packages.skims.docs.build;
  };
  name = "skims-docs-deploy";
  searchPaths = {
    envUtils = [ "/makes/utils/aws" ];
  };
  template = path "/makes/applications/skims/docs/deploy/entrypoint.sh";
}
