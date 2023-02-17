{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.google_sheets.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath fetchNixpkgs;
    observesIndex = inputs.observesIndex;
  };
  check = pkg.check.tests;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-etl-google-sheets-check-tests";
    entrypoint = "";
  }
