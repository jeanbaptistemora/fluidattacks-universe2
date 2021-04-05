{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-formstack;
  self = buildPythonPackage {
    name = "observes-tap-formstack";
    packagePath = path "/observes/singer/tap_formstack";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-formstack-runtime";
  searchPaths = {
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
      self
    ];
  };
}
