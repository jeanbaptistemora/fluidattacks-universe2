{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_bugsnag.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/singer/tap-bugsnag/env/runtime"
    ];
  };
  name = "observes-singer-tap-bugsnag-bin";
}
