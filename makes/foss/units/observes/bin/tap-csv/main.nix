{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_csv.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/singer/tap-csv/env/runtime"
    ];
  };
  name = "observes-bin-tap-csv";
}
