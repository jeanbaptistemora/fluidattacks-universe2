{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_timedoctor";
in
makeTemplate {
  name = "observes-env-tap-timedoctor-runtime";
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
