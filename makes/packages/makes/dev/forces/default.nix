{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "makes-dev-forces";
  searchPaths = {
    envSources = [
      packages.forces.config-development
      packages.forces.config-runtime
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
  template = path "/makes/packages/makes/dev/forces/template.sh";
}
