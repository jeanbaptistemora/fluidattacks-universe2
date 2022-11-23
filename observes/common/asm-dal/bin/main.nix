{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.common.asm_dal.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-common-asm-dal-env-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
