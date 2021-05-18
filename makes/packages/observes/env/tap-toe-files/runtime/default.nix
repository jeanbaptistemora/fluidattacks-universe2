{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_toe_files";
in
makeTemplate {
  name = "observes-env-tap-toe-files-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.python38
    ];
    envPythonPaths = [
      self
    ];
  };
}
