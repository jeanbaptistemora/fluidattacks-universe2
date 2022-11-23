{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.gitlab.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-singer-tap-gitlab-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
