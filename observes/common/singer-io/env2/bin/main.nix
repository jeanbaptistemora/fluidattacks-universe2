{
  fetchNixpkgs,
  makeTemplate,
  projectPath,
  ...
}: let
  root = projectPath "/observes/common/singer-io";
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-common-singer-io-env-bin";
    searchPaths = {
      bin = [
        env
      ];
    };
  }
