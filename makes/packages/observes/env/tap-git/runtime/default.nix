{ buildPythonPackage
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-tap-git";
    packagePath = path "/observes/singer/tap_git";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-git-runtime";
  searchPaths = {
    envPython38Paths = [
      self
    ];
  };
}
