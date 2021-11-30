{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_dynamo.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/singer/tap-dynamo/env/runtime"
    ];
  };
  name = "observes-singer-tap-dynamo-bin";
}
