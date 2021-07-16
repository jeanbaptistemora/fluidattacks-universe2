{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envImportLinterConfig = path "/skims/setup.imports.cfg";
    envSrcSkimsSkims = path "/skims/skims";
  };
  name = "skims-lint";
  searchPaths = {
    envSources = [
      packages.skims.test.mocks.http.env
      packages.skims.config-development
      packages.skims.config-runtime
      packages.skims.config-sdk
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
  template = path "/makes/applications/skims/lint/entrypoint.sh";
}
