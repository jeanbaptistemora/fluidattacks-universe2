{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-singer-io-development";
  searchPaths = {
    envPaths = [
      singer-io.development.python
    ];
    envPython38Paths = [
      singer-io.development.python
    ];
    envSources = [
      singer-io.runtime
    ];
  };
}
