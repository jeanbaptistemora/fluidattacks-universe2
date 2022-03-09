{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.csv.root;
in
  makeTemplate {
    name = "observes-singer-tap-csv-env-runtime";
    searchPaths = {
      pythonMypy = [
        self
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-singer-tap-csv-env-runtime";
          sourcesYaml = ./pypi-sources.yaml;
        })
        outputs."/observes/common/singer-io/env/runtime"
        outputs."/observes/common/purity/env/runtime"
      ];
    };
  }
