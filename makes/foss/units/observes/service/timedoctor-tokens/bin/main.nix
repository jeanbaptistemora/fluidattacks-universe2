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
      outputs."/observes/service/timedoctor-tokens/env/runtime"
    ];
  };
  name = "observes-service-timedoctor-tokens-bin";
}
