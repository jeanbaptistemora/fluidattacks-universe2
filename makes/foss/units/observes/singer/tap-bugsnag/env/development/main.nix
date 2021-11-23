{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-bugsnag-env-development";
  searchPaths = {
    source = [
      outputs."/observes/singer/tap-bugsnag/env/runtime"
    ];
  };
}
