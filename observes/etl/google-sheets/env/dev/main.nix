{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit fetchNixpkgs projectPath;
    observesIndex = inputs.observesIndex;
  };
  env = pkg.env.dev;
  bins = pkg.bin_deps;
in
  makeTemplate {
    name = "observes-etl-google-sheets-env-dev";
    searchPaths = {
      bin =
        bins
        ++ [
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
