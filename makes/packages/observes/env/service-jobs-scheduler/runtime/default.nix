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
      job.batch-stability
      scheduled.on-aws.bugsnag-etl
      scheduled.on-aws.checkly-etl
      scheduled.on-aws.code-etl-amend
      scheduled.on-aws.code-etl-mirror
      scheduled.on-aws.code-etl-upload
      scheduled.on-aws.delighted-etl
      scheduled.on-aws.dif-gitlab-etl
      scheduled.on-aws.dynamodb-forces-etl
      scheduled.on-aws.dynamodb-integrates-etl
      scheduled.on-aws.formstack-etl
      scheduled.on-aws.gitlab-etl.challenges
      scheduled.on-aws.gitlab-etl.default
      scheduled.on-aws.gitlab-etl.product
      scheduled.on-aws.gitlab-etl.services
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
