{ buildPythonPackage
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-tap-toe-files";
    packagePath = path "/observes/singer/tap_toe_files";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-toe-files-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envPython38Paths = [
      self
    ];
  };
}
