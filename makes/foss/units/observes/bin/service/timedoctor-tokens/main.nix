{ makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run timedoctor_tokens.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."/observes/env/service-timedoctor-tokens/runtime"
    ];
  };
  name = "observes-bin-service-timedoctor-tokens";
}
