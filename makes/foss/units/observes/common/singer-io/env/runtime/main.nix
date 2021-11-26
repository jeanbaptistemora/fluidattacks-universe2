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
  name = "observes-common-singer-io-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-common-singer-io-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/purity/env/runtime"
    ];
  };
}
