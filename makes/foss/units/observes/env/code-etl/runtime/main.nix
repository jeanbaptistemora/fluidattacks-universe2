{ inputs
, makePythonPypiEnvironment
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath "/observes/code_etl";
in
makeTemplate {
  name = "observes-env-code-etl-runtime";
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
        name = "observes-env-code-etl-runtime";
        sourcesYaml = ./pypi-sources.yaml;
        searchPaths = {
          bin = [
            inputs.nixpkgs.gcc
            inputs.nixpkgs.postgresql
          ];
        };
      })
    ];
  };
}
