{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-json-development";
  searchPaths = {
    envSources = [
      tap-json.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
