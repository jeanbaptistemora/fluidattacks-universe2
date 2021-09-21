{ makes
, makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/common/singer_io";
in
makeTemplate {
  name = "observes-env-singer-io-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-singer-io-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.purity.runtime
    ];
  };
}
