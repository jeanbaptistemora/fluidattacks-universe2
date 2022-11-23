{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_matomo main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.matomo.env.runtime}"
    ];
  };
  name = "observes-singer-tap-matomo-bin";
}
