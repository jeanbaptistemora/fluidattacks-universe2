{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.redshift.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.dev;
in
  makeTemplate {
    name = "observes-singer-target-redshift-env-dev";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
