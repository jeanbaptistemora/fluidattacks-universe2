{ inputs
, makeTemplate
, projectPath
, ...
}:
let
  self = projectPath inputs.observesIndex.tap.timedoctor.root;
in
makeTemplate {
  name = "observes-singer-tap-timedoctor-env-runtime";
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
