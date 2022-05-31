{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.common.asm_dal.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-common-asm-dal-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
