{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.s3.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.runtime;
in
  makeTemplate {
    name = "observes-singer-target-s3-env-runtime";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
