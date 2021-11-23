{ makeTemplate
, inputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_timedoctor";
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
