{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_toe_files main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/tap-toe-files/runtime"
    ];
  };
  name = "observes-bin-tap-toe-files";
}
