{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/sorts/assosiation-rules";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "sorts-assosiation-rules-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
