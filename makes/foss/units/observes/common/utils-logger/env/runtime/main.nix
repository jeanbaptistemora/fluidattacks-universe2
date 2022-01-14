{ inputs
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.utils_logger.root;
in
makeTemplate {
  name = "observes-common-utils-logger-env-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      outputs."${inputs.observesIndex.common.utils_logger.env.runtime}/python"
    ];
  };
}
