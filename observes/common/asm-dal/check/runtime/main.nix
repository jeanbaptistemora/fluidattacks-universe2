{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.common.asm_dal.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  check = pkg.check.runtime;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-common-asm-dal-check-runtime";
    entrypoint = "";
  }
