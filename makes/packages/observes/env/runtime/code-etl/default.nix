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
    name = "code-etl-env-runtime-python";
    requirements = {
      direct = [
        "aioextensions==20.9.2315218"
        "click==7.1.2"
        "GitPython==3.1.13"
        "ratelimiter==1.2.0"
        "requests==2.25.1"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==4.0.0"
        "gitdb==4.0.5"
        "idna==2.10"
        "smmap==3.0.5"
        "urllib3==1.26.3"
        "uvloop==0.14.0"
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
  name = "code-etl-env-runtime";
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
