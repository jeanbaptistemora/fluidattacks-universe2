{ makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = path "/observes/singer/tap_zoho_analytics";
in
makeTemplate {
  name = "observes-env-tap-zoho-analytics-runtime";
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
    envPython38Paths = [
      nixpkgs.python38Packages.requests
    ];
  };
}
