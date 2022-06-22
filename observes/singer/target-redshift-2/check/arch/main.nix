{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.redshift_2.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  check = pkg.check.arch;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-singer-target-redshift-check-arch";
    entrypoint = "";
  }
