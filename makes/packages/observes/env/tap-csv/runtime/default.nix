{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_csv";
in
makeTemplate {
  name = "observes-env-tap-csv-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.python38Packages.click
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.click
    ];
    envSources = [
      packages.observes.env.singer-io.runtime
      packages.observes.env.purity.runtime
    ];
  };
}
