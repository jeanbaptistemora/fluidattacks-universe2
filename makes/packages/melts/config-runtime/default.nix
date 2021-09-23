{ makes
, nixpkgs
, makeTemplate
, path
, ...
}:
let
  pythonRequirements = makes.makePythonPypiEnvironment {
    name = "melts-development";
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeTemplate {
  arguments = {
    envSrcMelts = path "/melts";
  };
  name = "melts-config-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.bash
      nixpkgs.cloc
      nixpkgs.git
      nixpkgs.nano
      nixpkgs.openssh
      nixpkgs.python38
      nixpkgs.sops
      nixpkgs.vim
    ];
    envPythonPaths = [
      (path "/melts")
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
    ];
    envSources = [
      pythonRequirements
      (makeTemplate {
        arguments = {
          envSrcMeltsStatic = path "/melts/static";
        };
        name = "melts-secrets-file";
        template = ''
          export MELTS_SECRETS='__envSrcMeltsStatic__/secrets.yaml'
        '';
      })
    ];
  };
  template = path "/makes/packages/melts/config-runtime/template.sh";
}
