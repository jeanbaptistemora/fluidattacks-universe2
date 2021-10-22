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
  name = "observes-env-tap-zoho-analytics-runtime";
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
      outputs."/observes/env/tap-zoho-analytics/runtime/python"
    ];
  };
}
