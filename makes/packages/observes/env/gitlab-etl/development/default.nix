{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-gitlab-etl-development";
  searchPaths = {
    envPython38Paths = [
      gitlab-etl.development.python
    ];
    envSources = [
      gitlab-etl.runtime
    ];
  };
}
