{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-bugsnag-env-development";
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.bugsnag.env.runtime}"
    ];
  };
}
