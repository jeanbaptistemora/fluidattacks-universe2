{
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.tap.zoho_analytics.root;
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
        outputs."${inputs.observesIndex.tap.zoho_analytics.env.runtime}/python"
      ];
    };
  }
