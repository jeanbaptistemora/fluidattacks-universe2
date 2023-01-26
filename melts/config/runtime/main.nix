{
  makePythonPypiEnvironment,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  pythonRequirements = makePythonPypiEnvironment {
    name = "melts-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsRuntime.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
    searchPathsBuild.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];

    # Required when using psycopg2 on Python3.8
    # Can be removed once we upgrade to Python3.9
    searchPathsBuild.export = [["CPATH" inputs.nixpkgs.libxcrypt "/include"]];
  };
in
  makeTemplate {
    replace = {
      __argSrcMelts__ = projectPath "/melts";
    };
    name = "melts-config-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.bash
        inputs.nixpkgs.cloc
        inputs.nixpkgs.git
        inputs.nixpkgs.gnutar
        inputs.nixpkgs.gzip
        inputs.nixpkgs.nano
        inputs.nixpkgs.openssh
        inputs.nixpkgs.python38
        inputs.nixpkgs.sops
        inputs.nixpkgs.vim
      ];
      pythonPackage = [
        (projectPath "/melts")
        (projectPath "/common/utils/bugsnag/client")
      ];
      source = [
        pythonRequirements
        (makeTemplate {
          replace = {
            __argSrcMeltsStatic__ = projectPath "/melts/static";
          };
          name = "melts-secrets-file";
          template = ''
            export MELTS_SECRETS='__argSrcMeltsStatic__/secrets.yaml'
          '';
        })
      ];
    };
    template = ./template.sh;
  }
