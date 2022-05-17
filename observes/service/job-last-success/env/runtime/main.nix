{
  makePythonPypiEnvironment,
  makeTemplate,
  inputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.service.job_last_success.root;
in
  makeTemplate {
    name = "observes-service-job-last-success-env-runtime";
    searchPaths = {
      pythonMypy = [
        self
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-service-job-last-success-env-runtime";
          searchPathsBuild.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
          searchPathsRuntime.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
          sourcesYaml = ./pypi-sources.yaml;
        })
      ];
    };
  }
