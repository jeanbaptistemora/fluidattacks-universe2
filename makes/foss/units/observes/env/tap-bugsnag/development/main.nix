{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-bugsnag-development";
  searchPaths = {
    source = [
      outputs."/observes/env/tap-bugsnag/runtime"
    ];
  };
}
