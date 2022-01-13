{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  entrypoint = ''
    import_and_run streamer_dynamodb main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.streamer_dynamodb.env.runtime}"
    ];
  };
  name = "observes-singer-streamer-dynamodb-bin";
}
