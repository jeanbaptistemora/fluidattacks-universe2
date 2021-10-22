{ makePythonPypiEnvironment
, makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_mixpanel";
in
makeTemplate {
  name = "observes-env-tap-mixpanel-runtime";
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
        name = "observes-env-tap-mixpanel-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-singer-io-runtime
    ];
  };
}
