{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-delighted-env-development";
  searchPaths = {
    source = [
      outputs."/observes/singer/tap-delighted/env/runtime"
    ];
  };
}
