{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-checkly-development";
  searchPaths = {
    source = [
      outputs."/observes/env/tap-checkly/runtime"
    ];
  };
}
