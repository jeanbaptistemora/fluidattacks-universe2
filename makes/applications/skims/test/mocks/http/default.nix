{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envApp = path "/makes/applications/skims/test/mocks/http";
  };
  name = "skims-test-mocks-http";
  template = path "/makes/applications/skims/test/mocks/http/entrypoint.sh";
  searchPaths = {
    envSources = [
      packages.skims.test.mocks.http.env
    ];
  };
}
