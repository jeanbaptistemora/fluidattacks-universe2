{ makePythonPypiEnvironment
, makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_git";
in
makeTemplate {
  name = "observes-env-tap-git-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    bin = [
      inputs.nixpkgs.git
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-git-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
