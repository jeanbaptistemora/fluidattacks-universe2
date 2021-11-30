{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-dynamo-env-development";
  searchPaths = {
    source = [
      outputs."/observes/singer/tap-dynamo/env/runtime"
    ];
  };
}
