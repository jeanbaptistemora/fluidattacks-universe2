{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_timedoctor main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.timedoctor.env.runtime}"
    ];
  };
  name = "observes-singer-tap-timedoctor-bin";
}
