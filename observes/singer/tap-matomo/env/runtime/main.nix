{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.matomo.root;
in
  makeTemplate {
    name = "observes-singer-tap-matomo-env-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.python38
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-singer-tap-matomo-env-runtime";
          sourcesYaml = ./pypi-sources.yaml;
        })
      ];
    };
  }
