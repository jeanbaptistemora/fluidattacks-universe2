{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/association-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "sorts-association-rules-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
