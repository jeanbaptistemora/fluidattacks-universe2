{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-checkly-env-development";
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.checkly.env.runtime}"
    ];
  };
}
