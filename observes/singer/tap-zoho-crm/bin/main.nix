{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    import_and_run streamer_zoho_crm.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.zoho_crm.env.runtime}"
    ];
  };
  name = "observes-singer-tap-zoho-crm-bin";
}
