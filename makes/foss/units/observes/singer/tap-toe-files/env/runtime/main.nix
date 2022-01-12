{ inputs
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.tap.toe_files.root;
in
makeTemplate {
  name = "observes-singer-tap-toe-env-files-runtime";
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
