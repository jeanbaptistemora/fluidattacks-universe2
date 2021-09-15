{ makePythonPypiEnvironment
, makeSearchPaths
, outputs
, ...
}:
let
  py_env = makePythonPypiEnvironment {
    name = "observes-env-tap-announcekit-dev";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeSearchPaths {
  source = [
    py_env
    outputs."/observes/singer/tap-announcekit/env/runtime"
  ];
}
