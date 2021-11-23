{ makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_formstack";
in
makeTemplate {
  name = "observes-singer-tap-formstack-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-formstack-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
