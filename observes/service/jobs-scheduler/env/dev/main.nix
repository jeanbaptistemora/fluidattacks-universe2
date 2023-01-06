{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-service-jobs-scheduler-env-runtime";
    searchPaths = {
      bin = [env];
      export = import ../bins.nix {inherit outputs;};
    };
    replace = {
      __argPython__ = inputs.nixpkgs.python310;
      __argPythonEnv__ = env;
      __argPythonEntry__ = ./vs_settings.py;
    };
    template = ./template.sh;
  }
