{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-checkly-development";
  searchPaths = {
    envSources = [
      tap-checkly.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
