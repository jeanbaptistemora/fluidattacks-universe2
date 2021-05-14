{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/services/job_last_success";
in
makeTemplate {
  name = "observes-env-job-last-success-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      job-last-success.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      job-last-success.runtime.python
    ];
  };
}
