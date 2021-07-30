{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-delighted-development";
  searchPaths = {
    envSources = [
      tap-delighted.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
