{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envImportLinterConfig = path "/skims/setup.imports.cfg";
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";

    envSrcProcessGroup = path "/makes/applications/skims/process-group/src";
    envSrcTestMocksHttp = path "/makes/applications/skims/test/mocks/http/src";
    envSrcSkimsTestSdk = path "/makes/applications/skims/test/sdk/src";
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
