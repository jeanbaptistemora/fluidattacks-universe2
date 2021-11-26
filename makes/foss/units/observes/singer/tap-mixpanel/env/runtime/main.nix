{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_mixpanel";
in
makeTemplate {
  name = "observes-singer-tap-mixpanel-env-runtime";
  searchPaths = {
    rpath = [
      inputs.nixpkgs.gcc.cc.lib
    ];
    pythonMypy = [
      self
    ];
    pythonPackage = [
      self
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-mixpanel-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/singer-io/env/runtime"
    ];
  };
}
