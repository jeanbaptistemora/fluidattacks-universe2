{
  fetchNixpkgs,
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  root = projectPath inputs.observesIndex.service.scheduler.root;
  pkg = import "${root}/entrypoint.nix" fetchNixpkgs projectPath inputs.observesIndex;
  env = pkg.env.bin;
in
  makeTemplate {
    name = "observes-service-jobs-scheduler-bin";
    searchPaths = {
      bin = [
        env
      ];
      source = [
        outputs."${inputs.observesIndex.service.scheduler.env.runtime}"
      ];
    };
  }
