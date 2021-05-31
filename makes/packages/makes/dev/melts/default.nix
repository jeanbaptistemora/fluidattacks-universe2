{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "makes-dev-melts";
  searchPaths = {
    envSources = [
      packages.melts.config-development
      packages.melts.config-runtime
    ];
  };
  template = path "/makes/packages/makes/dev/melts/template.sh";
}
