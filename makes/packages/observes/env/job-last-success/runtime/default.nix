{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.job-last-success;
  self = path "/observes/services/job_last_success";
in
makeTemplate {
  name = "observes-env-job-last-success-runtime";
  searchPaths = {
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      pkgEnv.runtime.python
    ];
  };
}
