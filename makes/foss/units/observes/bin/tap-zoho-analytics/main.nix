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
      outputs."/observes/singer/tap-zoho-analytics/env/runtime"
    ];
  };
  name = "observes-bin-tap-zoho-analytics";
}
