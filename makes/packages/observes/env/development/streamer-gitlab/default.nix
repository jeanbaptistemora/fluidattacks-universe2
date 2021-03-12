{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-development-streamer-gitlab-python";
    requirements = {
      direct = [
        "aioextensions==20.8.2087641"
        "aiohttp==3.6.2"
        "asgiref==3.2.10"
        "pytest-asyncio==0.14.0"
        "pytest==6.1.1"
      ];
      inherited = [
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "chardet==3.0.4"
        "idna==3.1"
        "iniconfig==1.1.1"
        "multidict==4.7.6"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "toml==0.10.2"
        "uvloop==0.14.0"
        "yarl==1.6.3"
      ];
    };
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-streamer-gitlab";
    packagePath = path "/observes/singer/streamer_gitlab";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-development-streamer-gitlab";
  searchPaths = {
    envPython38Paths = [
      pythonRequirements
      self
    ];
  };
}
