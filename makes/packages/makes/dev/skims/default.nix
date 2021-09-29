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
      packages.skims.config-runtime
    ];
    envPaths = [ nixpkgs.black ];
  };
  template = path "/makes/packages/makes/dev/skims/template.sh";
}
