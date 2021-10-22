{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_zoho_analytics.converter_zoho_csv cli "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/tap-zoho-analytics/runtime"
    ];
  };
  name = "observes-bin-tap-zoho-analytics";
}
