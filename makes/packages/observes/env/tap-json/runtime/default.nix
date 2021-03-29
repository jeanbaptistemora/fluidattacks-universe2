{ buildPythonPackage
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-tap-json";
    packagePath = path "/observes/singer/tap_json";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-json-runtime";
  searchPaths = {
    envPython38Paths = [
      self
    ];
  };
}
