{ inputs
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-dynamo-env-development";
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.dynamo.env.runtime}"
    ];
  };
}
