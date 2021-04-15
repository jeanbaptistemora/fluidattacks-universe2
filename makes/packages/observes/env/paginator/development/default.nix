{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-paginator-development";
  searchPaths = {
    envPaths = [
      paginator.development.python
    ];
    envPython38Paths = [
      paginator.development.python
    ];
    envSources = [
      paginator.runtime
    ];
  };
}
