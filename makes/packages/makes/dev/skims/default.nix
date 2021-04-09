{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "makes-dev-skims";
  searchPaths = {
    envSources = [
      packages.skims.test.mocks.http.env
      packages.skims.config-development
      packages.skims.config-runtime
    ];
  };
  template = path "/makes/packages/makes/dev/skims/template.sh";
}
