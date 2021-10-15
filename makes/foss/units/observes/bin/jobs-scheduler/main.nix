{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run jobs_scheduler main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/service-jobs-scheduler/runtime"
    ];
  };
  name = "observes-bin-service-jobs-scheduler";
}
