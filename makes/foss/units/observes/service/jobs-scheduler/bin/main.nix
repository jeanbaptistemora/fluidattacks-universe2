{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run jobs_scheduler.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/service/jobs-scheduler/env/runtime"
    ];
  };
  name = "observes-service-jobs-scheduler-bin";
}
