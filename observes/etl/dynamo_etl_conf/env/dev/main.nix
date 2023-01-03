{
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  system = "x86_64-linux";
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix.outputs.packages."${system}";
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-etl-dynamo-etl-conf-env-dev";
    searchPaths = {
      bin = [env];
    };
    replace = {
      __argPython__ = inputs.nixpkgs.python310;
      __argPythonEnv__ = env;
      __argPythonEntry__ = ./vs_settings.py;
    };
    template = ./template.sh;
  }
