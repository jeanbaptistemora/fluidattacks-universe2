{ buildPythonPackage
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-tap-timedoctor";
    packagePath = path "/observes/singer/tap_timedoctor";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-timedoctor-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envPython38Paths = [
      self
    ];
  };
}
