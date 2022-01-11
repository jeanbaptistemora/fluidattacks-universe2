{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_announcekit.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.announcekit.env.runtime}"
    ];
  };
  name = "observes-singer-tap-announcekit-bin";
}
