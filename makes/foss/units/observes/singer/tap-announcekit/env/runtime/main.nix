{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.tap.announcekit.root;
in
makeTemplate {
  name = "observes-singer-tap-announcekit-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-announcekit-env-runtime-python";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/paginator/env/runtime"
      outputs."/observes/common/purity/env/runtime"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
    ];
  };
}
