{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-runtime-tap-mailchimp-python";
    requirements = {
      direct = [
        "click==7.1.2"
        "mailchimp-marketing==3.0.31"
        "ratelimiter==1.2.0"
      ];
      inherited = [
        "bugsnag==4.0.2"
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "python-dateutil==2.8.1"
        "requests==2.25.1"
        "six==1.15.0"
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
  paginator = buildPythonPackage {
    name = "observes-paginator";
    packagePath = path "/observes/common/paginator";
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
  name = "observes-env-runtime-tap-mailchimp";
  searchPaths = {
    envPython38Paths = [
      logger
      paginator
      packages.observes.env.runtime.paginator.python
      pythonRequirements
      singerIO
      self
    ];
  };
}
