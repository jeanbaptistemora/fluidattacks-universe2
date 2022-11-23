{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-json-env-development";
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.json.env.runtime}"
    ];
  };
}
