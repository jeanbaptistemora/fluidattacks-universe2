{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-delighted-development";
  searchPaths = {
    source = [
      outputs."/observes/env/tap-delighted/runtime"
    ];
  };
}
