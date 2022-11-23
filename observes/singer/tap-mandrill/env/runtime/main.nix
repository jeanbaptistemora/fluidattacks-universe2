{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.mandrill.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-singer-tap-mandrill-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
