{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_formstack main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.formstack.env.runtime}"
    ];
  };
  name = "observes-singer-tap-formstack-bin";
}
