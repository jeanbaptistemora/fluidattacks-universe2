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
      outputs."/observes/env/job-last-success/runtime"
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-bin-service-job-last-success";
}
