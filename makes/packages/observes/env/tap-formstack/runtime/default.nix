{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pythonEnv = packages.observes.env.tap-formstack.runtime.python;
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
      pythonEnv
    ];
    envPython38Paths = [
      pythonEnv
      self
    ];
  };
}
