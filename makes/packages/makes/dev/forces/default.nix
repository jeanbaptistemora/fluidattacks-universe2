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
  };
  template = path "/makes/packages/makes/dev/forces/template.sh";
}
