{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.etl.code.root;
  pkg = import "${root}/entrypoint.nix" {
    inherit projectPath fetchNixpkgs;
    observesIndex = inputs.observesIndex;
  };
  check = pkg.check.types;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-etl-code-check-types";
    entrypoint = "";
  }
