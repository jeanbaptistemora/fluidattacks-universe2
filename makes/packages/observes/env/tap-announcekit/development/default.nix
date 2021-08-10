{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-announcekit-development";
  searchPaths = {
    envPaths = [
      tap-announcekit.development.python
    ];
    envPython38Paths = [
      tap-announcekit.development.python
    ];
    envSources = [
      tap-announcekit.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
