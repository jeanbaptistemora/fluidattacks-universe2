{ inputs
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.common.utils_logger.root;
  pkg = (inputs.flakeAdapter { src = self; }).defaultNix;
  env = pkg.outputs.packages.x86_64-linux.env.dev;
in
makeTemplate {
  name = "observes-common-utils-logger-flakes-env-dev";
  searchPaths = {
    bin = [ env ];
    pythonPackage = [
      self
    ];
  };
}
