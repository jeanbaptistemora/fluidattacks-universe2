{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes;
let
  self = path "/observes/services/jobs_scheduler";
in
makeTemplate {
  name = "observes-env-service-jobs-scheduler-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.python38
      scheduled.job.checkly-etl
      scheduled.job.delighted-etl
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      env.utils-logger.runtime
    ];
  };
}
