{ makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_toe_files";
in
makeTemplate {
  name = "observes-env-tap-toe-files-runtime";
  searchPaths = {
    pythonMypy = [
      self
    ];
    bin = [
      inputs.nixpkgs.python38
    ];
    pythonPackage = [
      self
    ];
  };
}
