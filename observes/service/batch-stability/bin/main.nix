{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.batch_stability.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-service-batch-stability-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
