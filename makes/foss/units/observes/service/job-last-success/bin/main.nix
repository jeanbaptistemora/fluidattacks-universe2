{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run job_last_success.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/service/job-last-success/env/runtime"
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-service-job-last-success-bin";
}
