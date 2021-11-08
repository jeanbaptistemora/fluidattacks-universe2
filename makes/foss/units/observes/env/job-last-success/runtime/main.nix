{ makePythonPypiEnvironment
, makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/services/job_last_success";
in
makeTemplate {
  name = "observes-env-job-last-success-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-job-last-success-runtime";
        searchPathsBuild.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
        searchPathsRuntime.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
