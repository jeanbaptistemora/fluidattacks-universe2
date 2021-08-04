{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-gitlab-development";
  searchPaths = {
    envPaths = [
      tap-gitlab.development.python
    ];
    envPython38Paths = [
      tap-gitlab.development.python
    ];
    envSources = [
      tap-gitlab.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}
