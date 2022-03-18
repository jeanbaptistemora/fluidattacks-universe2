{
  fetchNixpkgs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/main.nix" fetchNixpkgs projectPath inputs.observesIndex;
  check = pkg.check.types;
in
  makeScript {
    searchPaths = {
      bin = [check];
    };
    name = "observes-service-jobs-scheduler-lint";
    entrypoint = "";
  }
