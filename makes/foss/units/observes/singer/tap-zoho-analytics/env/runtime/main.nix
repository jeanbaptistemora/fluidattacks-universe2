{ makeTemplate
, inputs
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/singer/tap_zoho_analytics";
in
makeTemplate {
  name = "observes-singer-tap-zoho-env-analytics-runtime";
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
    source = [
      outputs."/observes/singer/tap-zoho-analytics/env/runtime/python"
    ];
  };
}
