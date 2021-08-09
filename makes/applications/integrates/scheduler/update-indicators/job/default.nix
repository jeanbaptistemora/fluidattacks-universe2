{ makeEntrypoint
, applications
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesScheduler = applications.integrates.scheduler;
  };
  name = "integrates-scheduler-update-indicators-job";
  template = path "/makes/applications/integrates/scheduler/update-indicators/job/entrypoint.sh";
}
