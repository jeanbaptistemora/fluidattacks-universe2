{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
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
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "idna==2.10"
        "python-dateutil==2.8.1"
        "requests==2.25.1"
        "six==1.15.0"
        "urllib3==1.26.3"
      ];
    };
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
      pythonRequirements
      singerIO
      self
    ];
  };
}
