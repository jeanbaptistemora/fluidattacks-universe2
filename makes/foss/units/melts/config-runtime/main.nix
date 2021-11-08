{ makePythonPypiEnvironment
, inputs
, makeTemplate
, projectPath
, ...
}:
let
  pythonRequirements = makePythonPypiEnvironment {
    name = "melts-development";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsRuntime.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
    searchPathsBuild.bin = [ inputs.nixpkgs.gcc inputs.nixpkgs.postgresql ];
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
      inputs.nixpkgs.nano
      inputs.nixpkgs.openssh
      inputs.nixpkgs.python38
      inputs.nixpkgs.sops
      inputs.nixpkgs.vim
    ];
    pythonPackage = [
      (projectPath "/melts")
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
          export MELTS_FLUIDCOUNTS_RULES='__argSrcMeltsStatic__/rules.def'
        '';
      })
    ];
  };
  template = ./template.sh;
}
