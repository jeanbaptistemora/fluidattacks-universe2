{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run code_etl.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/etl/code/env/runtime"
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-etl-code-bin";
}
