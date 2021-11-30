{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-checkly-env-development";
  searchPaths = {
    source = [
      outputs."/observes/singer/tap-checkly/env/runtime"
    ];
  };
}
