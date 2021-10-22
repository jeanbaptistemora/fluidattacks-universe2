{ makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/common/utils_logger";
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
