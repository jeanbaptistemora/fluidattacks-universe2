{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_json.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.json.env.runtime}"
    ];
  };
  name = "observes-singer-tap-json-bin";
}
