{ makes
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = path "/observes/services/job_last_success";
in
makeTemplate {
  name = "observes-env-job-last-success-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-job-last-success-runtime";
        searchPaths.bin = [ nixpkgs.gcc nixpkgs.postgresql ];
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}
