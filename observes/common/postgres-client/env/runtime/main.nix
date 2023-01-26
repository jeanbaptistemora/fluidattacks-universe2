{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.common.postgresClient;
in
  makeTemplate {
    name = "observes-common-postgres-client-env-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.postgresql
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-common-postgres-client-env-runtime";
          searchPathsRuntime.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
          searchPathsBuild.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
          sourcesYaml = ./pypi-sources.yaml;

          # Required when using psycopg2 on Python3.8
          # Can be removed once we upgrade to Python3.9
          searchPathsBuild.export = [["CPATH" inputs.nixpkgs.libxcrypt "/include"]];
        })
        outputs."/observes/common/purity/env/runtime"
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
      ];
    };
  }
