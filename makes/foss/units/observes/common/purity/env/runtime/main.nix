{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/purity";
in
makeTemplate {
  name = "observes-common-purity-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-common-purity-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
