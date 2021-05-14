{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-csv-development";
  searchPaths = {
    envPaths = [
      tap-csv.development.python
    ];
    envPython38Paths = [
      tap-csv.development.python
    ];
    envSources = [
      tap-csv.runtime
    ];
  };
}
