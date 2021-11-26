{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/code_etl";
in
makeTemplate {
  name = "observes-etl-code-env-runtime";
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
        name = "observes-etl-code-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
        searchPathsRuntime.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
        searchPathsBuild.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
      })
      outputs."/observes/common/purity/env/runtime"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
