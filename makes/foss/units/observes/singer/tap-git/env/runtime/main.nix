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
  name = "observes-singer-tap-git-env-runtime";
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
        name = "observes-singer-tap-git-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
