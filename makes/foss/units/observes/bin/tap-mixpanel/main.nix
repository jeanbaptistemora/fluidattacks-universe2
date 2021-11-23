{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_mixpanel main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/singer/tap-mixpanel/env/runtime"
    ];
  };
  name = "observes-bin-tap-mixpanel";
}
