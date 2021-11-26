{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/postgres_client";
in
makeTemplate {
  name = "observes-common-postgres-client-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    bin = [
      inputs.nixpkgs.postgresql
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-common-postgres-client-env-development";
        searchPathsRuntime.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
        searchPathsBuild.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
