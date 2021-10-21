{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "observes-env-tap-json-development";
  searchPaths = {
    source = [
      outputs."/observes/env/tap-json/runtime"
    ];
  };
}
