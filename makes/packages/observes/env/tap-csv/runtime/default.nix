{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-csv;
  self = buildPythonPackage {
    name = "observes-tap-csv";
    packagePath = path "/observes/singer/tap_csv";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-csv-runtime";
  searchPaths = {
    envSources = [
      env.runtime.singer-io
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
      self
    ];
  };
}
