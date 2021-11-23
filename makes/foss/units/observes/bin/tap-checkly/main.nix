{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_checkly.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/singer/tap-checkly/env/runtime"
    ];
  };
  name = "observes-bin-tap-checkly";
}
