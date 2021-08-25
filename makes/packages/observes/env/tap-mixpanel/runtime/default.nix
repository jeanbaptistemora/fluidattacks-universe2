{ makes
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_mixpanel";
in
makeTemplate {
  name = "observes-env-tap-mixpanel-runtime";
  searchPaths = {
    envLibraries = [
      nixpkgs.gcc.cc.lib
    ];
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-mixpanel-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      packages.observes.env.singer-io.runtime
    ];
  };
}
