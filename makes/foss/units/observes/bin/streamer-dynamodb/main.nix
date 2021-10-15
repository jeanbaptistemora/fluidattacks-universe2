{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  entrypoint = "import_and_run streamer_dynamodb main";
  searchPaths = {
    source = [
      outputs."/observes/commin/import-and-run"
      inputs.product.observes.env.streamer-dynamodb.runtime
    ];
  };
  name = "observes-bin-streamer-dynamodb";
}
