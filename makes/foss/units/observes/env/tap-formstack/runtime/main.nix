{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_formstack";
in
makeTemplate {
  name = "observes-env-tap-formstack-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-formstack-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
