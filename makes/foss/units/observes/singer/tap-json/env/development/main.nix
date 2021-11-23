{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-singer-tap-json-env-development";
  searchPaths = {
    source = [
      outputs."/observes/singer/tap-json/env/runtime"
    ];
  };
}
