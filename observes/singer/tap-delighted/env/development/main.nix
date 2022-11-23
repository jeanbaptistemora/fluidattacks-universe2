{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-delighted-env-development";
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.delighted.env.runtime}"
    ];
  };
}
