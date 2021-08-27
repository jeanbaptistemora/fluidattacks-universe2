{ makeTemplate
, packages
, path
, nixpkgs
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
    envPaths = [ nixpkgs.black ];
  };
  template = path "/makes/packages/makes/dev/skims/template.sh";
}
