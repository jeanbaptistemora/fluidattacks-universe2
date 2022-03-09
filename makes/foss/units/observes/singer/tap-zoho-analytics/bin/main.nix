{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_zoho_analytics.converter_zoho_csv cli "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.zoho_analytics.env.runtime}"
    ];
  };
  name = "observes-singer-tap-zoho-analytics-bin";
}
