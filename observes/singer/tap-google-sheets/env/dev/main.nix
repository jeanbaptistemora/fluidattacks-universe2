{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs;
  };
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-tap-google-sheets-env-dev";
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
