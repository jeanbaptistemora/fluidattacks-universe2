{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run target_redshift.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/target-redshift/runtime"
    ];
  };
  name = "observes-target-redshift";
}
