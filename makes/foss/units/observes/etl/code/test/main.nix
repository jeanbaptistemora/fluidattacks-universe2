{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.code.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  check = pkg.check.tests;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-etl-code-test";
    entrypoint = "";
  }
