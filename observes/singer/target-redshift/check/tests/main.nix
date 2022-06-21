{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.target.redshift.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  check = pkg.check.tests;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-singer-target-redshift-check-tests";
    entrypoint = "";
  }
