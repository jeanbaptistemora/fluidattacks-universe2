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
      scheduled.on-aws.code-etl-amend
      scheduled.on-aws.code-etl-mirror
      scheduled.on-aws.code-etl-upload
      scheduled.on-aws.dif-gitlab-etl
      scheduled.on-aws.formstack-etl
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
