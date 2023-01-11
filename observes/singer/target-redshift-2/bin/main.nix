{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.redshift_2.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "target-redshift";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = "target-redshift \"\${@}\"";
  }
