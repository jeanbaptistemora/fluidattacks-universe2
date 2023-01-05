{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.success_indicators.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeScript {
    name = "success-indicators";
    searchPaths = {
      bin = [
        env
      ];
    };
    entrypoint = "success-indicators \"\${@}\"";
  }
