{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/purity";
in
makeTemplate {
  name = "observes-env-purity-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-purity-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
