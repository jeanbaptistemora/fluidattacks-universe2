{ inputs
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.utilsLogger;
in
makeTemplate {
  name = "observes-env-utils-logger-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      outputs."/observes/env/utils-logger/runtime/python"
    ];
  };
}
