{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pkgSrc = path "/observes/etl/dif_gitlab_etl";
  pythonRequirements = buildPythonRequirements {
    name = "dif-gitlab-etl-env-development-python";
    requirements = {
      direct = [
        "aiohttp==3.6.2"
        "click==7.1.2"
        "nest-asyncio==1.4.1"
      ];
      inherited = [
        "aioextensions==20.8.2087641"
        "asgiref==3.2.10"
        "async-timeout==3.0.1"
        "attrs==20.3.0"
        "chardet==3.0.4"
        "idna==3.1"
        "multidict==4.7.6"
        "uvloop==0.14.0"
        "yarl==1.6.3"
      ];
    };
    python = nixpkgs.python38;
  };
  streamerGitlab = buildPythonPackage {
    name = "observes-streamer-gitlab";
    packagePath = path "/observes/singer/streamer_gitlab";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-dif-gitlab-etl";
    packagePath = pkgSrc;
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "dif-gitlab-etl-env-development";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.python38Packages.psycopg2
      pythonRequirements
      self
      streamerGitlab
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      pythonRequirements
      self
      streamerGitlab
    ];
  };
}
