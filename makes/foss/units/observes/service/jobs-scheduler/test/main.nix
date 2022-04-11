{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  check = pkg.check.tests;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-service-jobs-scheduler-test";
    entrypoint = "";
  }
