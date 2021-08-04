{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-announcekit-development";
  searchPaths = {
    envSources = [
      tap-announcekit.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
