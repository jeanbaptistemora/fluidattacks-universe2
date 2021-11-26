{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/singer_io";
in
makeTemplate {
  name = "observes-env-singer-io-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-singer-io-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/purity/env/runtime"
    ];
  };
}
