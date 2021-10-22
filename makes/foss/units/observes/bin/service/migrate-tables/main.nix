{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run migrate_tables.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/env/service-migrate-tables/runtime"
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-bin-service-migrate-tables";
}
