{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/paginator";
in
makeTemplate {
  name = "observes-env-paginator-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-paginator-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/purity/env/runtime"
    ];
  };
}
