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
      outputs."/observes/env/tap-mixpanel/runtime"
    ];
  };
  name = "observes-bin-tap-mixpanel";
}
