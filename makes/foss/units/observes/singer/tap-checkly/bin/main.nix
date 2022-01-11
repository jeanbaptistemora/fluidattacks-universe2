{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_checkly.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.checkly.env.runtime}"
    ];
  };
  name = "observes-singer-tap-checkly-bin";
}
