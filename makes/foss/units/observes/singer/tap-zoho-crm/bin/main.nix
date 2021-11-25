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
      outputs."/observes/singer/tap-zoho-crm/env/runtime"
    ];
  };
  name = "observes-singer-tap-zoho-crm-bin";
}
