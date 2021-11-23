{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_delighted";
in
makeTemplate {
  name = "observes-singer-tap-delighted-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-delighted-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
      outputs."/observes/env/singer-io/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
