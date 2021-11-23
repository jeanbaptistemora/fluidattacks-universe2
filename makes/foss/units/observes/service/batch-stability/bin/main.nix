{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run batch_stability.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/service/batch-stability/env/runtime"
    ];
  };
  name = "observes-service-batch-stability-bin";
}
