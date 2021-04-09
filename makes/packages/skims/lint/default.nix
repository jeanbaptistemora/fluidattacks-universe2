{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envImportLinterConfig = path "/skims/setup.imports.cfg";
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";

    envSrcProcessGroup = path "/makes/applications/skims/process-group/src";
    envSrcTestMocksHttp = path "/makes/applications/skims/test/mocks/http/src";
  };
  builder = path "/makes/packages/skims/lint/builder.sh";
  name = "skims-lint";
  searchPaths = {
    envSources = [
      packages.skims.test.mocks.http.env
      packages.skims.config-development
      packages.skims.config-runtime
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
