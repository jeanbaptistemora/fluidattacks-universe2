{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_delighted.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/singer/tap-delighted/env/runtime"
    ];
  };
  name = "observes-bin-tap-delighted";
}
