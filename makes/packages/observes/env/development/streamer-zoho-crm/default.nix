{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-development-streamer-zoho-crm-python";
    requirements = {
      direct = [
        "click==7.1.2"
        "pytest-postgresql==2.5.2"
        "pytest==5.2.0"
        "ratelimiter==1.2.0"
        "requests==2.25.0"
      ];
      inherited = [
        "atomicwrites==1.4.0"
        "attrs==20.3.0"
        "certifi==2020.12.5"
        "chardet==3.0.4"
        "idna==2.10"
        "mirakuru==2.3.0"
        "more-itertools==8.6.0"
        "packaging==20.9"
        "pluggy==0.13.1"
        "port-for==0.4"
        "psutil==5.8.0"
        "py==1.10.0"
        "pyparsing==2.4.7"
        "urllib3==1.26.3"
        "wcwidth==0.2.5"
      ];
    };
    python = nixpkgs.python38;
  };
  postgresClient = buildPythonPackage {
    name = "observes-streamer-zoho-crm";
    packagePath = path "/observes/common/postgres_client";
    python = nixpkgs.python38;
  };
  singerIO = buildPythonPackage {
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-streamer-zoho-crm";
    packagePath = path "/observes/singer/streamer_zoho_crm";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-development-streamer-zoho-crm";
  searchPaths = {
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      pythonRequirements
      postgresClient
      singerIO
      self
    ];
  };
}
