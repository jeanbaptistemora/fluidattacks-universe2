{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "tap-zoho-analytics-env-development-python";
    requirements = {
      direct = [
        "requests==2.25.1"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "urllib3==1.26.3"
      ];
    };
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-tap-zoho-analytics";
    packagePath = path "/observes/singer/tap_zoho_analytics";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "tap-zoho-analytics-env-development";
  searchPaths = {
    envPaths = [
      pythonRequirements
      self
    ];
    envPython38Paths = [
      pythonRequirements
      self
    ];
  };
}
