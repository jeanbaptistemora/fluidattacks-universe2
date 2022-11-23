{
  fetchNixpkgs,
  makeScript,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/association-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.bin;
in
  makeScript {
    searchPaths = {
      bin = [
        env
      ];
      source = [
        outputs."/common/utils/aws"
        outputs."/common/utils/sops"
      ];
    };
    name = "sorts-association-rules-bin";
    entrypoint = ./entrypoint.sh;
  }
