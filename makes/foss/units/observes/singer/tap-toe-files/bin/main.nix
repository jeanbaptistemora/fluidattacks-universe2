{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_toe_files main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.toe_files.env.runtime}"
    ];
  };
  name = "observes-singer-tap-toe-files-bin";
}
