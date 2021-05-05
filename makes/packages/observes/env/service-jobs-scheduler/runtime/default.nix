{ makeTemplate
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
      env.service-jobs-scheduler.runtime.python
      scheduled.job.checkly-etl
      scheduled.job.delighted-etl
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      env.service-jobs-scheduler.runtime.python
    ];
    envSources = [
      env.utils-logger.runtime
    ];
  };
}
