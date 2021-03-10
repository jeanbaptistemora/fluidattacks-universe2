{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pkgSrc = path "/observes/code_etl";
  pythonRequirements = buildPythonRequirements {
    name = "code-etl-env-development-python";
    requirements = {
      direct = [
        "aioextensions==20.9.2315218"
        "click==7.1.2"
        "GitPython==3.1.13"
        "pytest-asyncio==0.14.0"
        "pytest==6.2.2"
        "ratelimiter==1.2.0"
        "requests==2.25.1"
      ];
      inherited = [
        "attrs==20.3.0"
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "gitdb==4.0.5"
        "idna==2.10"
        "iniconfig==1.1.1"
        "packaging==20.9"
        "pluggy==0.13.1"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "smmap==3.0.5"
        "toml==0.10.2"
        "urllib3==1.26.3"
        "uvloop==0.15.2"
      ];
    };
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-code-etl";
    packagePath = pkgSrc;
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "code-etl-env-development";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.python38Packages.psycopg2
      pythonRequirements
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      pythonRequirements
      self
    ];
  };
}
