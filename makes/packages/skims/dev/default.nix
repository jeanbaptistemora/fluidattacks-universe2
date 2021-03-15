{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "skims-dev";
  searchPaths = {
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
  };
  template = path "/makes/packages/skims/dev/template.sh";
}
