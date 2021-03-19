{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-development-tap-mailchimp-python";
    requirements = {
      direct = [
        "click==7.1.2"
        "mailchimp-marketing==3.0.31"
        "pytest==6.2.2"
      ];
      inherited = [
        "attrs==20.3.0"
        "bugsnag==4.0.2"
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "iniconfig==1.1.1"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "python-dateutil==2.8.1"
        "requests==2.25.1"
        "six==1.15.0"
        "toml==0.10.2"
        "urllib3==1.26.3"
        "WebOb==1.8.7"
      ];
    };
    python = nixpkgs.python38;
  };
  logger = buildPythonPackage {
    name = "observes-utils-logger";
    packagePath = path "/observes/common/utils_logger";
    python = nixpkgs.python38;
  };
  singerIO = buildPythonPackage {
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-tap-mailchimp";
    packagePath = path "/observes/singer/tap_mailchimp";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-development-tap-mailchimp";
  searchPaths = {
    envPaths = [
      pythonRequirements
    ];
    envPython38Paths = [
      logger
      pythonRequirements
      singerIO
      self
    ];
    envMypy38Paths = [
      logger
      singerIO
      self
    ];
  };
}
