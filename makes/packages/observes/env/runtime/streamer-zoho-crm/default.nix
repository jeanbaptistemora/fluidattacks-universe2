{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-runtime-streamer-zoho-crm-python";
    requirements = {
      direct = [
        "click==7.1.2"
        "ratelimiter==1.2.0"
        "requests==2.25.0"
      ];
      inherited = [
        "certifi==2020.12.5"
        "chardet==3.0.4"
        "idna==2.10"
        "urllib3==1.26.3"
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
  name = "observes-env-runtime-streamer-zoho-crm";
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
