{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run streamer_zoho_crm.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/streamer-zoho-crm/runtime"
    ];
  };
  name = "observes-bin-streamer-zoho-crm";
}
