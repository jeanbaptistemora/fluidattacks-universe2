{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-code-etl-development";
  searchPaths = {
    envPaths = [
      code-etl.development.python
    ];
    envPython38Paths = [
      code-etl.development.python
    ];
    envSources = [
      code-etl.runtime
    ];
  };
}
