{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.job_last_success.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-service-job-last-success-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
    replace = {
      __argPython__ = inputs.nixpkgs.python310;
      __argPythonEnv__ = env;
      __argPythonEntry__ = ./vs_settings.py;
    };
    template = ./template.sh;
  }
