{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.tap.gitlab.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  check = pkg.check.arch;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-singer-tap-gitlab-check-arch";
    entrypoint = "";
  }
