{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-bugsnag-development";
  searchPaths = {
    envSources = [
      tap-bugsnag.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
