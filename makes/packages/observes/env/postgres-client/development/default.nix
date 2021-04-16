{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-postgres-client-development";
  searchPaths = {
    envPaths = [
      postgres-client.development.python
    ];
    envPython38Paths = [
      postgres-client.development.python
    ];
    envSources = [
      postgres-client.runtime
    ];
  };
}
