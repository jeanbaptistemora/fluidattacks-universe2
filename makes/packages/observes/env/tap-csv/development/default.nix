{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pythonEnv = packages.observes.env.tap-csv.development.python;
  singerIO = buildPythonPackage {
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-tap-csv";
    packagePath = path "/observes/singer/tap_csv";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-csv-development";
  searchPaths = {
    envPaths = [
      pythonEnv
    ];
    envPython38Paths = [
      pythonEnv
      singerIO
      self
    ];
  };
}
